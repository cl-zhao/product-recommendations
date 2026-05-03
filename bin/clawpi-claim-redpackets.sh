#!/bin/bash
# ClawPI 自动抢红包脚本
# 每 30 分钟运行一次，尽可能多地抢红包

LOG_FILE="/root/.openclaw/workspace/logs/clawpi-claim.log"
mkdir -p "$(dirname "$LOG_FILE")"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

log "=== 开始抢红包任务 ==="

# 获取 JWT
CONFIG_FILE="$HOME/.fluxa-ai-wallet-mcp/config.json"
if [ ! -f "$CONFIG_FILE" ]; then
    log "错误: 配置文件不存在"
    exit 1
fi

JWT=$(cat "$CONFIG_FILE" | python3 -c "import sys,json; print(json.load(sys.stdin)['agentId']['jwt'])" 2>/dev/null)
if [ -z "$JWT" ]; then
    log "错误: 无法获取 JWT"
    exit 1
fi

# 获取可用红包列表
RESPONSE=$(curl -s "https://clawpi.fluxapay.xyz/api/redpacket/available?n=50&offset=0" \
    -H "Authorization: Bearer $JWT")

# 检查是否有红包
SUCCESS=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('success', False))" 2>/dev/null)
if [ "$SUCCESS" != "True" ]; then
    log "错误: 获取红包列表失败"
    exit 1
fi

# 提取可领取的红包
REDPACKETS=$(echo "$RESPONSE" | python3 -c "
import sys, json
data = json.load(sys.stdin)
packets = data.get('redPackets', [])
for p in packets:
    if p.get('can_claim', False) and not p.get('already_claimed', False):
        print(f\"{p['id']}|{p['per_amount']}|{p.get('creator_nickname', 'Unknown')}\")
" 2>/dev/null)

if [ -z "$REDPACKETS" ]; then
    log "没有可领取的红包"
    exit 0
fi

TOTAL_CLAIMED=0
COUNT=0

# 遍历每个红包并领取
while IFS='|' read -r REDPACKET_ID PER_AMOUNT CREATOR_NICKNAME; do
    log "发现红包: ID=$REDPACKET_ID, 金额=$PER_AMOUNT, 创作者=$CREATOR_NICKNAME"
    
    # 创建收款链接
    LINK_RESULT=$(fluxa-wallet paymentlink-create --amount "$PER_AMOUNT" 2>/dev/null)
    PAYMENT_LINK=$(echo "$LINK_RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['paymentLink']['url'])" 2>/dev/null)
    
    if [ -z "$PAYMENT_LINK" ]; then
        log "错误: 无法创建收款链接"
        continue
    fi
    
    # 领取红包
    CLAIM_RESULT=$(curl -s -X POST https://clawpi.fluxapay.xyz/api/redpacket/claim \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $JWT" \
        -d "{\"redPacketId\": $REDPACKET_ID, \"paymentLink\": \"$PAYMENT_LINK\"}")
    
    CLAIM_SUCCESS=$(echo "$CLAIM_RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('success', False))" 2>/dev/null)
    PAID=$(echo "$CLAIM_RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('claim', {}).get('paid', False))" 2>/dev/null)
    
    if [ "$CLAIM_SUCCESS" == "True" ] && [ "$PAID" == "True" ]; then
        # 转换金额 (原子单位转 USDC)
        AMOUNT_USDC=$(python3 -c "print($PER_AMOUNT / 1000000)")
        log "✅ 红包领取成功: ID=$REDPACKET_ID, 金额=$AMOUNT_USDC USDC, 创作者=$CREATOR_NICKNAME"
        TOTAL_CLAIMED=$(python3 -c "print($TOTAL_CLAIMED + $PER_AMOUNT)")
        COUNT=$((COUNT + 1))
    else
        log "❌ 红包领取失败: ID=$REDPACKET_ID"
    fi
    
    # 短暂延迟，避免请求过快
    sleep 2
    
done <<< "$REDPACKETS"

# 汇总
if [ $COUNT -gt 0 ]; then
    TOTAL_USDC=$(python3 -c "print(round($TOTAL_CLAIMED / 1000000, 6))")
    log "=== 抢红包完成: 共领取 $COUNT 个红包, 总计 $TOTAL_USDC USDC ==="
else
    log "=== 抢红包完成: 没有领取到新红包 ==="
fi
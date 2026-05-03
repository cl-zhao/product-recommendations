# -*- coding: utf-8 -*-
from __future__ import annotations

import os
from typing import List

import numpy as np
import onnxruntime as ort
from tokenizers import Tokenizer


class EmbeddingError(Exception):
    pass


class BGEEmbedder:
    def __init__(
        self,
        model_path: str,
        tokenizer_path: str,
        max_length: int = 512,
        normalize: bool = True,
        intra_threads: int = 2,
        inter_threads: int = 1,
    ) -> None:
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"ONNX model not found: {model_path}")
        if not os.path.exists(tokenizer_path):
            raise FileNotFoundError(f"Tokenizer not found: {tokenizer_path}")

        self.tokenizer = Tokenizer.from_file(tokenizer_path)
        self.max_length = max_length
        self.normalize = normalize

        sess_options = ort.SessionOptions()
        sess_options.intra_op_num_threads = intra_threads
        sess_options.inter_op_num_threads = inter_threads
        sess_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL

        self.session = ort.InferenceSession(
            model_path,
            sess_options=sess_options,
            providers=["CPUExecutionProvider"],
        )
        self.input_names = [x.name for x in self.session.get_inputs()]
        self.output_names = [x.name for x in self.session.get_outputs()]
        self.output_name = self.output_names[0]
        self.dim = int(self.session.get_outputs()[0].shape[-1])

    def _tokenize(self, texts: List[str]) -> dict:
        input_ids = []
        attention_mask = []
        token_type_ids = []

        for text in texts:
            if not isinstance(text, str):
                raise EmbeddingError("Input text must be str")
            text = text.strip() or " "
            enc = self.tokenizer.encode(text)
            ids = enc.ids[: self.max_length]
            type_ids = (enc.type_ids or [0] * len(ids))[: self.max_length]
            mask = [1] * len(ids)
            pad_len = self.max_length - len(ids)
            if pad_len > 0:
                ids += [0] * pad_len
                type_ids += [0] * pad_len
                mask += [0] * pad_len
            input_ids.append(ids)
            attention_mask.append(mask)
            token_type_ids.append(type_ids)

        features = {
            "input_ids": np.asarray(input_ids, dtype=np.int64),
            "attention_mask": np.asarray(attention_mask, dtype=np.int64),
        }
        if "token_type_ids" in self.input_names:
            features["token_type_ids"] = np.asarray(token_type_ids, dtype=np.int64)
        return features

    @staticmethod
    def _mean_pooling(last_hidden_state: np.ndarray, attention_mask: np.ndarray) -> np.ndarray:
        mask = attention_mask[..., None].astype(np.float32)
        masked = last_hidden_state * mask
        summed = masked.sum(axis=1)
        counts = np.clip(mask.sum(axis=1), a_min=1e-9, a_max=None)
        return summed / counts

    def embed_batch(self, texts: List[str]) -> np.ndarray:
        if not texts:
            return np.empty((0, self.dim), dtype=np.float32)
        try:
            inputs = self._tokenize(texts)
            outputs = self.session.run([self.output_name], inputs)[0]
            emb = self._mean_pooling(outputs, inputs["attention_mask"]).astype(np.float32)
            if self.normalize:
                norms = np.linalg.norm(emb, axis=1, keepdims=True)
                emb = emb / np.clip(norms, 1e-12, None)
            return emb
        except Exception as e:
            raise EmbeddingError(f"embed_batch failed: {e}") from e

    def embed_one(self, text: str) -> np.ndarray:
        vectors = self.embed_batch([text])
        if vectors.shape[0] == 0:
            raise EmbeddingError("empty embedding result")
        return vectors[0]

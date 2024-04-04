import torch
from transformers import BartForConditionalGeneration

class QuantizedBART(BartForConditionalGeneration):
    def __init__(self, config):
        super().__init__(config)
        self.quant = torch.quantization.QuantStub()
        self.dequant = torch.quantization.DeQuantStub()
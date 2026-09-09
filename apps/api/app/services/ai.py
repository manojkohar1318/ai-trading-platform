from abc import ABC, abstractmethod
class LLMProvider(ABC):
    @abstractmethod
    def generate(self,system:str,user:str,context:dict)->str: ...
class MockLLMProvider(LLMProvider):
    def generate(self,system,user,context):
        return "DEMO AI response: quantitative analysis is available, but no live LLM provider is configured."
class TradingAIService:
    def __init__(self,llm:LLMProvider): self.llm=llm
    def answer(self,question,analysis=None):
        return self.llm.generate("You are a trading analysis assistant. Never guarantee outcomes.",question,analysis or {})

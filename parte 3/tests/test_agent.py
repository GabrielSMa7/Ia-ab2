import json

from src.agent import Agent, SYSTEM_PROMPT


def test_agent_initialization():
    agent = Agent()
    assert agent.messages[0]["role"] == "system"
    assert agent.messages[0]["content"] == SYSTEM_PROMPT
    assert "web_search" in agent.tools
    assert len(agent.tools) == 1


def test_parse_response_json_answer():
    agent = Agent()
    text = '{"answer": "Olá! Como posso ajudar?"}'
    result = agent._parse_response(text)
    assert result["answer"] == "Olá! Como posso ajudar?"


def test_parse_response_json_tool_call():
    agent = Agent()
    text = '{"tool": "web_search", "args": {"query": "clima hoje"}}'
    result = agent._parse_response(text)
    assert result["tool"] == "web_search"
    assert result["args"]["query"] == "clima hoje"


def test_parse_response_with_code_block():
    agent = Agent()
    text = "```json\n{\"answer\": \"Resposta dentro de bloco\"}\n```"
    result = agent._parse_response(text)
    assert result["answer"] == "Resposta dentro de bloco"


def test_parse_response_plain_text():
    agent = Agent()
    text = "Qualquer texto sem JSON"
    result = agent._parse_response(text)
    assert result["answer"] == "Qualquer texto sem JSON"


def test_reset():
    agent = Agent()
    agent.messages.append({"role": "user", "content": "Olá"})
    agent.messages.append({"role": "assistant", "content": '{"answer": "Oi!"}'})
    assert len(agent.messages) == 3
    agent.reset()
    assert len(agent.messages) == 1
    assert agent.messages[0]["role"] == "system"

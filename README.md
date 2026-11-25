# TechFix: Triagem Inteligente (Sistema Especialista)

**Empresa simulada:** TechFix Assistência Técnica (celulares e notebooks).
**Problema:** a triagem varia de atendente para atendente. O sistema padroniza o diagnóstico, define a urgência e explica o raciocínio.

## Como rodar
```
python sistema_especialista.py   # sistema
python testes.py                 # testes
```
Não precisa instalar nada além do Python.

## Como funciona
- **Fatos:** frases curtas como `liga`, `nao_liga`, `liquido`. As respostas do usuário viram fatos.
- **Regras (27):** `SE condições ENTÃO conclusão`. Ficam na lista `REGRAS`.
- **Motor (encadeamento para frente):** função `inferir`. Aplica as regras até não surgir fato novo. As conclusões de uma regra podem ser condição de outra (ex.: `liquido` → `suspeita_oxidacao` → `diag_liquido` → `urgencia_alta`).
- **Explicação:** `pq` numa pergunta mostra por que ela é feita (`por_que`). Depois do resultado, `como` mostra a cadeia de regras usada.
- **Exceções:** entrada inválida repete a pergunta; sem diagnóstico, mostra "não foi possível concluir...".

"""Голосовий агент-помічник піцерії.

Стек: LiveKit Agents (Worker + AgentSession) + OpenAI Realtime API (gpt-realtime-mini).
Агент веде голосовий чат українською: показує меню, розповідає про страви,
оформлює та відстежує замовлення. Tools підключені з fake_api.py.

Запуск:
    python agent.py console   # локальний мікрофон/динаміки (потрібен лише OPENAI_API_KEY)
"""

from __future__ import annotations

from dotenv import load_dotenv
from livekit import agents
from livekit.agents import Agent, AgentSession, JobContext, WorkerOptions
from livekit.plugins import openai

from tools import ALL_TOOLS

load_dotenv()


INSTRUCTIONS = """\
Ти — Ксенія, голосова помічниця піцерії «Везувіо». Ти спілкуєшся з клієнтом по телефону
і допомагаєш обрати страву, оформити та відстежити замовлення.

Як ти говориш:
- Тільки українською мовою, тепло й привітно, як справжній оператор.
- Коротко й природно: одне-два речення за раз. Це голосова розмова.
- Без markdown, без списків зі зірочками чи дефісами, без емодзі. Перелічуй усно,
  через кому або «а ще».
- Ціни називай словами зрозуміло, напр. «сто вісімдесят дев'ять гривень».

Завжди звіряйся з даними через інструменти — не вигадуй позицій, цін чи статусів.

Оформлення замовлення:
- Збери позиції з кількістю, ім'я клієнта, телефон і адресу доставки.
- Якщо страва недоступна (available = false), чесно скажи про це і запропонуй заміну.
- Перед викликом create_order стисло повтори замовлення вголос і дочекайся підтвердження.
- Після оформлення назви номер замовлення, суму та орієнтовний час доставки.

Статус замовлення:
- Уточни номер у форматі ORD-101, потім виклич get_order_status.

Не вигадуй позицій, цін чи статусів, яких немає у відповідях tools. Якщо чогось немає
в меню — скажи про це прямо.
"""


class PizzaAgent(Agent):
    def __init__(self) -> None:
        super().__init__(instructions=INSTRUCTIONS, tools=ALL_TOOLS)


async def entrypoint(ctx: JobContext) -> None:
    session = AgentSession(
        llm=openai.realtime.RealtimeModel(
            model="gpt-realtime-mini",
            voice="marin",
        ),
    )

    await session.start(agent=PizzaAgent(), room=ctx.room)

    await session.generate_reply(
        instructions=(
            "Привітайся українською від імені піцерії «Везувіо», коротко й тепло. "
            "Запитай, чим можеш допомогти: показати меню чи оформити замовлення."
        ),
    )


if __name__ == "__main__":
    agents.cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))

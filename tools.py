"""Function tools для голосового агента піцерії.

Тонкі обгортки навколо `fake_api.py`: вони лише підключають готові функції
до агента через LiveKit function calling. Сам `fake_api.py` не змінюється.

З docstring та типів аргументів LiveKit генерує JSON-схему, яку OpenAI Realtime
використовує, щоб вирішити, коли і з якими параметрами викликати функцію.
"""

from __future__ import annotations

from typing import Any, Literal, TypedDict

from livekit.agents import RunContext, function_tool

import fake_api


class OrderItem(TypedDict):
    """Одна позиція замовлення."""

    id: str  # ідентифікатор позиції меню, напр. "pz1"
    quantity: int  # кількість, напр. 2


@function_tool
async def get_menu(
    ctx: RunContext,
    category: Literal["pizza", "drinks", "desserts"] | None = None,
) -> list[dict[str, Any]]:
    """Показати меню піцерії або окрему категорію.

    Викликай, коли клієнт просить меню чи питає, що є з піц, напоїв або десертів.

    Args:
        category: Категорія для фільтра — "pizza", "drinks" або "desserts".
            Якщо не вказано, повертає все меню.
    """
    return fake_api.get_menu(category)


@function_tool
async def get_item_details(ctx: RunContext, item_id: str) -> dict[str, Any]:
    """Отримати повну інформацію про конкретну страву: склад, ціну, розмір, наявність.

    Викликай, коли клієнт хоче деталі про конкретну позицію. Спершу візьми її
    ідентифікатор (item_id, напр. "pz1") з результату get_menu.

    Args:
        item_id: Ідентифікатор позиції меню, напр. "pz1".
    """
    return fake_api.get_item_details(item_id)


@function_tool
async def create_order(
    ctx: RunContext,
    items: list[OrderItem],
    customer_name: str,
    phone: str,
    address: str,
) -> dict[str, Any]:
    """Оформити замовлення.

    Викликай лише після того, як зібрав і проговорив для підтвердження всі дані:
    позиції з кількістю, ім'я, телефон та адресу доставки.

    Args:
        items: Список позицій замовлення, кожна — {"id": "pz1", "quantity": 2}.
        customer_name: Ім'я клієнта.
        phone: Контактний телефон.
        address: Адреса доставки.
    """
    return fake_api.create_order(
        items=[dict(i) for i in items],
        customer_name=customer_name,
        phone=phone,
        address=address,
    )


@function_tool
async def get_order_status(ctx: RunContext, order_id: str) -> dict[str, Any]:
    """Перевірити статус замовлення за його номером.

    Викликай, коли клієнт питає, що з його замовленням. Спершу уточни номер
    у форматі "ORD-101".

    Args:
        order_id: Номер замовлення, напр. "ORD-101".
    """
    return fake_api.get_order_status(order_id)


# Список усіх tools для передачі в Agent(tools=...).
ALL_TOOLS = [get_menu, get_item_details, create_order, get_order_status]

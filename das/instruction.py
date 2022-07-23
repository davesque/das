from __future__ import annotations

from typing import TYPE_CHECKING, Iterator

from das.exceptions import RenderedError
from das.parser import Op
from das.utils import byte_length

if TYPE_CHECKING:  # pragma: no cover
    from das.compiler import Compiler


class BaseInstruction:
    __slots__ = ("compiler",)

    compiler: Compiler

    def __init__(self, compiler: Compiler):
        self.compiler = compiler
        self.validate()

    def validate(self) -> None:  # pragma: no cover
        raise NotImplementedError("must define `validate`")

    def encode(self) -> Iterator[int]:  # pragma: no cover
        raise NotImplementedError("must define `encode`")

    @property
    def size(self) -> int:  # pragma: no cover
        raise NotImplementedError("must define `size`")


class Instruction(BaseInstruction):
    __slots__ = ("op",)

    mnemonic: str = None  # type: ignore
    op: Op

    def __init__(self, compiler: Compiler, op: Op):
        self.op = op
        super().__init__(compiler)


class Nullary(Instruction):
    def validate(self) -> None:
        if self.op.arg is not None:
            raise RenderedError(
                f"'{self.mnemonic}' instruction takes no argument",
                self.op.toks,
            )


class Unary(Instruction):
    def validate(self) -> None:
        if self.op.arg is None:
            raise RenderedError(
                f"'{self.mnemonic}' instruction requires an argument",
                self.op.toks,
            )


class Const(Nullary):
    output: int = None  # type: ignore

    def encode(self) -> Iterator[int]:
        yield self.output

    @property
    def size(self) -> int:
        return byte_length(self.output)

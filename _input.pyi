"""
存根
"""

global_time: float


# 鼠标操作
class Mouse(object):
    @staticmethod
    def move(
            x: int = None,
            y: int = None,
            relative_if: bool = False,
            before_time: float = global_time,
            after_time: float = global_time
    ) -> bool: ...

    @staticmethod
    def down(
            x: int = None,
            y: int = None,
            loop: int = 1,
            button: int = 0,
            before_time: float = global_time,
            after_time: float = global_time,
            loop_before_time: float = global_time,
            loop_after_time: float = global_time,
    ) -> bool: ...

    @staticmethod
    def hold_down(
            x: int = None,
            y: int = None,
            button: int = 0,
            before_time: float = global_time,
            after_time: float = global_time,
    ) -> bool: ...

    @staticmethod
    def hold_up(
            x: int = None,
            y: int = None,
            button: int = 0,
            before_time: float = global_time,
            after_time: float = global_time,
    ) -> bool: ...

    @staticmethod
    def hold_re(
            x: int = None,
            y: int = None,
            button: int = 0,
            before_time: float = global_time,
            after_time: float = global_time,
    ) -> bool: ...

    @staticmethod
    def drag(
            start_x: int = None,
            start_y: int = None,
            end_x: int = None,
            end_y: int = None,
            loop: int = 1,
            button: int = 0,
            before_time: float = global_time,
            after_time: float = global_time,
            loop_before_time: float = global_time,
            loop_after_time: float = global_time,
            smooth_if: bool = False,
            smooth_time: float = global_time,
            smooth_count: int = None
    ) -> bool: ...


class Key(object):
    @staticmethod
    def down(
            key: int,
            loop: int = 1,
            before_time: float = global_time,
            after_time: float = global_time,
            loop_before_time: float = global_time,
            loop_after_time: float = global_time,
    ) -> bool: ...

    @staticmethod
    def hold_down(
            key: int,
            before_time: float = global_time,
            after_time: float = global_time,
    ) -> bool: ...

    @staticmethod
    def hold_up(
            key: int,
            before_time: float = global_time,
            after_time: float = global_time,
    ) -> bool: ...

    @staticmethod
    def hold_re(
            key: int,
            before_time: float = global_time,
            after_time: float = global_time,
    ) -> bool: ...

    class Down(object):
        @staticmethod
        def all(
                key: int | list,
                loop: int = 1,
                before_time: float = global_time,
                after_time: float = global_time,
                loop_before_time: float = global_time,
                loop_after_time: float = global_time,
                down_before_time: float = global_time,
                down_after_time: float = global_time,
                in_key_check: bool = True
        ) -> bool: ...

        @staticmethod
        def all_shift(
                key: int | list,
                loop: int = 1,
                before_time: float = global_time,
                after_time: float = global_time,
                loop_before_time: float = global_time,
                loop_after_time: float = global_time,
                down_before_time: float = global_time,
                down_after_time: float = global_time,
                in_key_check: bool = True
        ) -> bool: ...

    class Return(object):
        @staticmethod
        def _int(_str: str | list[str]) -> bool | list[int]: ...

        @staticmethod
        def _int_strs(_str: str) -> bool | list[int]: ...

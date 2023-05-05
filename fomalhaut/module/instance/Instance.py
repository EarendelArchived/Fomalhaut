import discord as _main
from asyncio import sleep as _timeout

from .handlers.ActivityHandler import ActivityHandler as _Activity
from .handlers.message.embed import ColourElement as _Colour
from .handlers.message.embed import Embed as _Embed
from .handlers.message.embed import FieldElement as _Field
from .handlers.message.embed import FooterElement as _Footer
from ..core import Final as _Final
from ..core import Functional as _Functional
from ..core import Nullable as _Nullable
from ..logutils.ExceptionHandler import ExceptionHandler as _ExcHandler
from ..logutils.LogUtils import HandledMessage as _HandledMsg
from ..logutils.LogUtils import LogUtils as _LogUtils
from ...main.settings import Settings as _Settings


class Instance(_main.Client):
    """
    기본값이 초기화된 인스턴스를 생성합니다.
    
    Parameters
    -----------
    group: str
        인스턴스 설정 그룹
    name: str
        인스턴스 이름
    settings: Settings
        메인 핸들 설정
    activity: ActivityHandler
        인스턴스 활동
        
    Attributes
    -----------
    name: str
        인스턴스 이름
    main: Settings
        메인 핸들 설정
    settings: dict
        인스턴스 설정
    logger: LogUtils
        인스턴스 로거
    """

    def __init__(
            self, settings: _Settings, group: str, name: str, activity: _Activity, timeout: int = 5
    ) -> None:
        logger: _Final[_LogUtils] = _LogUtils(name)
        handler: _Final[_ExcHandler] = _ExcHandler(logger, settings)
        logger.log("인스턴스를 초기화 하는중...")
        try:
            super().__init__(intents=_main.Intents.all())

            self.name: _Final[str] = name
            self.main: _Final[_Settings] = settings
            self.settings: _Final[dict] = settings.get("instance", group, name)
            self._activity: _Activity = activity
            self._footer: _Nullable[_Footer] = None

            self.logger: _Final[_LogUtils] = logger
            self._exc_handler: _Final[_ExcHandler] = handler

            self._tasks: list[list[_Functional, bool]] = []
            self._timeout: _Final[int] = timeout
            self.schedules()

            self.tree: _Final[_main.app_commands.CommandTree] = _main.app_commands.CommandTree(self)
            self.commands()

            @self.tree.command(name="sync", description="명령어를 동기화합니다.")
            async def this(interaction: _main.Interaction) -> None:
                async def that() -> None:
                    await interaction.followup.send(
                        embed=_Embed(title="성공적으로 동기화 요청을 보냈습니다.", colour=_Colour.green())
                    )
                    await self.tree.sync()
                await self.process(interaction, that)

        except Exception as e:
            handler.handle(e, "init").throw()
            return
        logger.log("인스턴스를 초기화 했습니다.")

        try:
            logger.log("서버에 연결하는 중...")
            self.run(self.settings['token'])
        except Exception as e:
            handler.handle(e, "run").throw()
            return

    @property
    def footer(self):
        return self._footer

    def schedules(self) -> None:
        pass

    def commands(self) -> None:
        pass

    def schedule(self, task: _Functional) -> None:
        self._tasks.append([task, True])

    def group(self, name: str, description: str) -> _Functional:
        def decorator(main: _Functional) -> None:
            result: _main.app_commands.Group = _main.app_commands.Group(name=name, description=description)
            main(result)
            self.tree.add_command(result)

        return decorator

    async def process(self, interaction: _main.Interaction, func: _Functional) -> None:
        # noinspection PyUnresolvedReferences
        await interaction.response.defer()
        try:
            await func()
        except Exception as e:
            handled: _HandledMsg = self.handle_exc(e, f"Command.{interaction.command.name}")
            if handled.file is None:
                await interaction.followup.send(embed=handled.embed)
            else:
                await interaction.followup.send(embed=handled.embed, file=handled.file)

    async def send(self, handled: _HandledMsg) -> None:
        """
        핸들링된 메세지를 로그 채널에 전송합니다.
        
        Parameters
        ----------
        handled: HandledMessage
            핸들링된 메세지
        """
        try:
            self.logger.log(handled.content)
            await self.send_to("", self.main.instance.logger['target'].send, embed=handled.embed, file=handled.file)
        except Exception as e:
            await self.throw(e, "send", additional=_Field("Log value", handled.content))

    async def log(self, content: str) -> None:
        """
        로그 채널에 메세지를 전송합니다.
        
        Parameters
        ----------
        content: str
            전송할 메세지
        """
        await self.send(_HandledMsg(content, embed=_Embed(title=content, colour=_Colour.green(), footer=self.footer)))

    def handle_exc(
            self, exception: Exception, location: str, additional: _Nullable[_Field] = None, ignored: bool = False
    ) -> _HandledMsg:
        """
        발생한 예외를 처리하여 HandledMessage 형태로 반환합니다.

        Parameters
        ----------
        exception: Exception
            발생한 예외
        location: str
            예외가 발생한 위치
        additional: Optional[FieldElement]
            추가적으로 보낼 필드
        ignored: bool
            예외를 무시할지 여부
        """
        handled: _Final[_HandledMsg] = self._exc_handler.handle(
            exception, location, additional=additional, ignored=ignored
        ).get()

        self.logger.log(handled.content)
        return handled

    async def throw(
            self, exception: Exception, location: str, additional: _Nullable[_Field] = None, ignored: bool = False,
            bypass_try: bool = False
    ) -> _Nullable[_HandledMsg]:
        """
        발생한 예외를 처리하여 로그 채널에 전송합니다.
        
        Parameters
        ----------
        exception: Exception
            발생한 예외
        location: str
            예외가 발생한 위치
        additional: Optional[FieldElement]
            추가적으로 보낼 필드
        ignored: bool
            예외를 무시할지 여부
        bypass_try: bool
            인스턴스 전송을 시도하는것을 무시할지 여부
        """
        handled: _Final[_ExcHandler] = self._exc_handler.handle(
            exception, location, additional=additional, ignored=ignored
        )

        if bypass_try:
            handled.throw()
        else:
            try:
                await self.send(handled.get())
            except Exception as e:
                handled.throw()
                self._exc_handler.handle(e, "throw").throw()
        return

    async def send_to(
            self, message: str, channel_id: list[int] = None, edit_target: list[list[int]] = None, embed: _Embed = None,
            file: _main.File = None,
    ) -> list[list[int]]:
        """
        채널에 메세지를 보냅니다.

        Parameters
        ----------
        message: str
            메세지
        channel_id: Optional[list[int]]
            메세지를 보낼 채널 ID 리스트
        edit_target: Optional[list[list[int]]]
            메세지를 수정할 대상 리스트
        embed: Optional[EmbedElement]
            메세지에 포함할 Embed
        file: Optional[discord.File]
            메세지에 포함할 파일
        """
        value: list[list[int]] = []
        if channel_id is not None:
            for i in channel_id:
                target: _Nullable[_main.TextChannel] = self.get_channel(i)
                if target is not None:
                    value.append(
                        [i, (await target.send(message, embed=embed, file=file)).id]
                    )
        elif edit_target is not None:
            for i in edit_target:
                target: _Nullable[_main.TextChannel] = self.get_channel(i[0])
                if target is not None:
                    await (await target.fetch_message(i[1])).edit(
                        content=message, embed=embed, attachments=[file]
                    )
                    value.append([i[0], i[1]])
        return value

    async def _tick(self) -> None:
        """
        스케줄러를 시작합니다.
        """
        if self._tasks:
            await _timeout(0)
            status: bool = True
            while status:
                run: bool = False
                for i in self._tasks:
                    if i[1]:
                        i[1] = await i[0]()
                        run = True
                status = run
                await _timeout(self._timeout)

    async def wait_until_ready(self) -> None:
        """
        인스턴스가 준비될때까지 기다립니다.
        """
        try:
            await super().wait_until_ready()
            self.logger.log("인스턴스 최적화가 완료되었습니다.")
        except Exception as e:
            await self.throw(e, "wait_until_ready")

    async def on_connect(self) -> None:
        """
        인스턴스가 서버에 연결되면 호출됩니다.
        """
        self.logger.log("서버에 연결되었습니다.")

    async def on_ready(self) -> None:
        """
        인스턴스가 준비되면 호출됩니다.
        """
        try:
            self.logger.log("인스턴스를 시작하는 중...")
            await self.wait_until_ready()

            await self.change_presence(
                activity=_main.Activity(type=self._activity.type, name=self._activity.content),
                status=self._activity.status
            )
            self._footer = _Footer(self.user.name, self.user.display_avatar.url)

            await self.log("인스턴스를 시작했습니다.")
            await self._tick()
        except Exception as e:
            await self.throw(e, "on_ready")

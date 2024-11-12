import click
from tools import constants as C
from tools.h3c.cli import h3c

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.pass_context
def cli(ctx):
    # 将配置传递到上下文中
    ctx.ensure_object(dict)
    ctx.obj["config"] = C  # 将配置字典存储到上下文对象中


@cli.command()
@click.pass_context
def show(ctx):
    """查看配置信息"""
    # 访问上下文中的配置
    config = ctx.obj["config"]
    click.echo(f"H3C Address: {config.h3c_address}")


# 注册子命令
cli.add_command(h3c)


if __name__ == "__main__":
    cli()

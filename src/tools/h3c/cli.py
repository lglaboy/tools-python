import click
import tools.constants as C
from tools.h3c import aes_cipher
from tools.h3c.api import H3C

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option("--address", default=C.h3c_address)
@click.option("--flag", default=C.h3c_flag)
@click.pass_context
def h3c(ctx, address, flag):

    ctx.ensure_object(dict)

    ctx.obj["address"] = address
    ctx.obj["flag"] = flag
    # click.echo(f"address: {address}")


@h3c.command()
@click.pass_context
def show(ctx):
    """查看配置信息"""
    # 访问上下文中的配置
    address = ctx.obj["address"]
    click.echo(f"h3c address: {address}")


@h3c.command()
@click.option("-u", "--user", required=True)
@click.option("-p", "--password", required=True)
@click.pass_context
def flag_encrypt(ctx, user, password):
    f = aes_cipher.encrypt_user_password(user, password)
    click.echo(f)


@h3c.command()
@click.option("-f", "--flag", required=True)
@click.pass_context
def flag_decrypt(ctx, flag):
    u, p = aes_cipher.decrypt_user_password(flag)

    click.echo(u)
    click.echo(p)


@h3c.group()
@click.pass_context
def get(ctx):
    pass


@get.command()
@click.pass_context
def user(ctx):
    address = ctx.obj["address"]
    flag = ctx.obj["flag"]

    client = H3C(address, flag)
    client.get_local_user()


@h3c.group()
@click.pass_context
def create(ctx):
    pass


@create.command()
@click.pass_context
@click.option("-n", "--name", required=True, help="Name of new h3c user")
@click.option("-p", "--password", help="Password of new h3c user")
# @click.option("--sslvpn", default=False, is_flag=True, help="Enable SSLVPN")
def user(ctx, name, password):
    """
    创建用户，默认开启SSLVPN，密码不指定会自动生成8位随机密码
    """
    address = ctx.obj["address"]
    flag = ctx.obj["flag"]

    sslvpn = True

    client = H3C(address, flag)
    client.create_local_user(name, password, sslvpn)


@h3c.group()
@click.pass_context
def delete(ctx):
    pass


@delete.command()
@click.pass_context
@click.option("-n", "--name", required=True, help="delete user name")
def user(ctx, name):
    """
    删除用户
    """
    address = ctx.obj["address"]
    flag = ctx.obj["flag"]

    client = H3C(address, flag)
    client.delete_local_user(name)

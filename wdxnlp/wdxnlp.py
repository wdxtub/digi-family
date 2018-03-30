import click
import utils.text_util as tu
import utils.os_util as ou


@click.group()
@click.version_option()
def cli():
    """wdxnlp
    来自 wdx 的自然语言处理工具包，感谢无师对我的大力支持
    """

# ====================== basic group =======================
@cli.group()
def basic():
    """自然语言处理的基础功能，如分词、词性等"""

@basic.command("segmentation")
@click.argument('input_file', type=click.File('rb'))
@click.argument('output_file', type=click.File('wb'))
@click.option('--user_dict', '-d', default='./data/dict/jieba_user.dict',
              help="用户自定词典，默认为 ./data/dict/jieba_user.dict")
@click.option('--seperator', '-s', default=' ',
              help="分隔词语的分隔符，默认为空格")
@click.option('--output_encoding', '-oe', default='utf8',
              help="输出文件的编码，默认为 utf8")
def segmentation(input_file, output_file, user_dict, seperator, output_encoding):
    ou.check_ret(tu.segementation(input_file, output_file, user_dict, seperator, output_encoding))


# ====================== advance group =======================


@cli.group()
def ship():
    """Manages ships."""


@ship.command('new')
@click.argument('name')
def ship_new(name):
    """Creates a new ship."""
    click.echo('Created ship %s' % name)


@ship.command('move')
@click.argument('ship')
@click.argument('x', type=float)
@click.argument('y', type=float)
@click.option('--speed', metavar='KN', default=10,
              help='Speed in knots.')
def ship_move(ship, x, y, speed):
    """Moves SHIP to the new location X,Y."""
    click.echo('Moving ship %s to %s,%s with speed %s' % (ship, x, y, speed))


@ship.command('shoot')
@click.argument('ship')
@click.argument('x', type=float)
@click.argument('y', type=float)
def ship_shoot(ship, x, y):
    """Makes SHIP fire to X,Y."""
    click.echo('Ship %s fires to %s,%s' % (ship, x, y))


@cli.group('mine')
def mine():
    """Manages mines."""


@mine.command('set')
@click.argument('x', type=float)
@click.argument('y', type=float)
@click.option('ty', '--moored', flag_value='moored',
              default=True,
              help='Moored (anchored) mine. Default.')
@click.option('ty', '--drifting', flag_value='drifting',
              help='Drifting mine.')
def mine_set(x, y, ty):
    """Sets a mine at a specific coordinate."""
    click.echo('Set %s mine at %s,%s' % (ty, x, y))


@mine.command('remove')
@click.argument('x', type=float)
@click.argument('y', type=float)
def mine_remove(x, y):
    """Removes a mine at a specific coordinate."""
    click.echo('Removed mine at %s,%s' % (x, y))
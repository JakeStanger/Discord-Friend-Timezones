import discord
import pytz
from datetime import datetime
from discord.ext import commands
from fuzzywuzzy import process
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json

with open('settings.json', 'r') as f:
    settings = json.loads(f.read())

engine = create_engine(settings['database'])
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class UserZone(Base):
    __tablename__ = 'UserZone'

    id = Column(Integer, primary_key=True)
    zone = Column(String)


Base.metadata.create_all(engine)


def get_or_create(model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


bot = commands.Bot(command_prefix=settings['prefix'])


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.command(name='tzset')
async def set_zone(ctx, *, timezone):
    if timezone in pytz.all_timezones:
        zone = timezone
    else:
        zone = process.extractOne(timezone, pytz.all_timezones)[0]

    user_zone = get_or_create(UserZone, id=ctx.author.id)
    user_zone.zone = zone
    session.commit()

    await ctx.send("Set to **%s**" % zone)


def query_zone(user: discord.Member):
    zone = session.query(UserZone).filter_by(id=user.id).first()

    if zone:
        return zone.zone
    else:
        return 'Not set'


def get_zone_time(zone: str):
    if zone == 'Not set':
        return zone

    tz = pytz.timezone(zone)
    return tz.normalize(datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(tz)).strftime('%H:%M')


@set_zone.error
async def info_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please specify a timezone')
    else:
        print(error)


@bot.command(name='tzget')
async def get_zone(ctx, users: commands.Greedy[discord.Member]):
    if len(users) == 0:
        return await ctx.send("You must mention at least one user")

    await ctx.send('\n'.join([
        '%s: **%s**' % (user.nick or user.name,
                        query_zone(user))
        for user in set(users)
    ]))


@bot.command(name='time')
async def get_time(ctx, users: commands.Greedy[discord.Member]):
    if len(users) == 0:
        return await ctx.send("You must mention at least one user")

    await ctx.send('\n'.join([
        '%s: **%s**' % (user.nick or user.name,
                        get_zone_time(query_zone(user)))
        for user in set(users)
    ]))

bot.run(settings['token'])
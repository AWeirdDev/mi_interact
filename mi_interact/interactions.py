import random
import string


class InteractionError(Exception):
  """Interaction Errors, 包含:
  - 404
  - 403
  ... (other :flushed:)
  """
  pass


class MI(object):
  def __init__(self, client, channel_id: int):
    self._data = {}
    self._client = client
    self._ch_id = channel_id
    self._session = self._generate()
    try:
      self._client.get_channel(channel_id)
    except:
      raise InteractionError(f"找不到此頻道！")

  def _generate(self, size=15):
    lmao = string.ascii_uppercase + string.ascii_lowercase + string.digits
    return ''.join(random.choice(lmao) for _ in range(size))

  async def get_user_data(self, user_id: int):
    def check(m):
      return m.author.id == 955828209860112395 and m.channel.id == self._ch_id
    channel = self._client.get_channel(self._ch_id)
    await channel.send(f"MI.get_user_data {user_id} {self._session}")
    res = await self._client.wait_for("message", check=check)
    if res.content == f"MI.user_data none {self._session}":
      return None
    elif res.content == f"你因為在1分鐘內發送超過45個請求，所以你的請求會被Mine Bot拒絕5分鐘 ({self._session})":
      raise InteractionError(
        f"你因為在1分鐘內發送超過45個請求，所以你的請求會被Mine Bot拒絕5分鐘 (Session ID: {self._session})"
      )
    content = res.content.replace(f"MI.user_data ", "")
    content = content.split("|")
    class UserObject(object):
      pass

    setattr(UserObject, "id", int(content[0]))
    setattr(UserObject, "pickaxe", content[1])
    setattr(UserObject, "backpack", content[2])
    setattr(UserObject, "m_coin", content[3])
    setattr(UserObject, "field", content[4])
    setattr(UserObject, "exp", content[5])
    setattr(UserObject, "level", content[6])
    setattr(UserObject, "count", content[7])
    setattr(UserObject, "guild", content[8])
    setattr(UserObject, "mystery_stone", content[9])
    setattr(UserObject, "miner_level", content[10])
    setattr(UserObject, "miner_skill_1", content[11])
    setattr(UserObject, "miner_skill_2", content[12])
    setattr(UserObject, "miner_skill_3", content[13])
    return UserObject

  @property
  def connect_id(self):
    return self._session

  @property
  def channel_id(self):
    return self._ch_id

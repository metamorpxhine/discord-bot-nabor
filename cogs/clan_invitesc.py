import disnake
from disnake.ext import commands


class NoButtons(disnake.ui.View):
	def __init__(self):
		super().__init__(timeout=None)

	@disnake.ui.button(label="Принять", style=disnake.ButtonStyle.green, custom_id="disaccept", disabled=True)
	async def button1(self, button, interaction: disnake.MessageInteraction):
		await interaction.response.defer()

	@disnake.ui.button(label="Отклонить", style=disnake.ButtonStyle.red, custom_id="disdecline", disabled=True)
	async def button2(self, button, interaction: disnake.MessageInteraction):
		await interaction.response.defer()




class DeclineReason(disnake.ui.Modal):
	def __init__(self, author, name, age, reason, rate):
		self.author = author
		self.name = name
		self.age = age
		self.reason = reason
		self.rate = rate
		components = [
			disnake.ui.TextInput(label="Причина:", placeholder="Рофл заявка, Неккоректная заявка",  custom_id="reason")
		]
		super().__init__(title="Отклонение заявки в клан", components=components, custom_id="declinereason")

	async def callback(self, interaction: disnake.ModalInteraction) -> None:
		reason = interaction.text_values["reason"]
		embed = disnake.Embed(title=f"Заявка в клан")
		embed.set_thumbnail(url=f'{interaction.author.display_avatar.url}')
		embed.add_field(name=f"**Отклонил:**", value=f'{interaction.author.mention}', inline=False)
		embed.add_field(name=f"**Причина:**", value=f'{reason}', inline=False)
		embed.add_field(name=f"**Подал:**", value=f"{self.author.mention}", inline=False)
		embed.add_field(name=f"**Имя:**", value=f"```{self.name}```", inline=False)
		embed.add_field(name=f"**Возраст:**", value=f"```{self.age}```", inline=False)
		embed.add_field(name=f"**Умения:**", value=f"```{self.reason}```", inline=False)
		embed.add_field(name=f"**Оценка умений:**", value=f"```{self.rate}```", inline=False)
		embed.set_image(url=f"https://cdn.discordapp.com/attachments/772218365413818428/1079003352408543302/11112.png?ex=65993aae&is=6586c5ae&hm=ce8a40820a148e8b6b639c8fec30d75cdc3f7e3f0726729d47f1d93e9b0ed26f&")
		await interaction.message.edit(embed=embed, view=NoButtons())
		await interaction.response.send_message(f"Заявка отклонена", ephemeral=True)
		await self.author.send(embed=embed)



class ClanButtons(disnake.ui.View):
	def __init__(self, author, name, age, reason, rate):
		self.author = author
		self.name = name
		self.age = age
		self.reason = reason
		self.rate = rate
		super().__init__(timeout=None)

	@disnake.ui.button(label="Принять", style=disnake.ButtonStyle.green, custom_id="accept")
	async def button1(self, button, interaction: disnake.MessageInteraction):
		if interaction.author.get_role(1221858474850390127) == None:
			await interaction.response.defer()
		else:
			emb = disnake.Embed()
			emb.description = f'Поздравляю, ты принят в клан.\n' \
					f'Ставь приписку клана в ник - social'
			emb.set_image(url=f"https://cdn.discordapp.com/attachments/1211275021713014854/1224093847890559099/image_10.png?ex=661c3d3b&is=6609c83b&hm=e0207f3964274b2a842c457a9d68f27c46db1f2b012d266d7e2bf9a547a1e250&")
			embed = disnake.Embed(title=f"Заявка в клан")
			embed.set_thumbnail(url=f'{interaction.author.display_avatar.url}')
			embed.add_field(name=f"**Принял:**", value=f'{interaction.author.mention}', inline=False)
			embed.add_field(name=f"**Подал:**", value=f"{self.author.mention}", inline=False)
			embed.add_field(name=f"**Имя:**", value=f"```{self.name}```", inline=False)
			embed.add_field(name=f"**Возраст:**", value=f"```{self.age}```", inline=False)
			embed.add_field(name=f"**Умения:**", value=f"```{self.reason}```", inline=False)
			embed.add_field(name=f"**Оценка умений:**", value=f"```{self.rate}```", inline=False)
			embed.set_image(url=f"https://cdn.discordapp.com/attachments/1211275021713014854/1224093847890559099/image_10.png?ex=661c3d3b&is=6609c83b&hm=e0207f3964274b2a842c457a9d68f27c46db1f2b012d266d7e2bf9a547a1e250&")
			await interaction.message.edit(embed=embed, view=NoButtons())
			await interaction.response.send_message(f"Заявка принята", ephemeral=True)
			await self.author.send(embed=emb)
			role = interaction.guild.get_role(1221856943887482931)
			await self.author.add_roles(role)

#Айди роли чтобы принимать в клан
	@disnake.ui.button(label="Отклонить", style=disnake.ButtonStyle.red, custom_id="decline")
	async def button2(self, button, interaction: disnake.MessageInteraction):
		if interaction.author.get_role(1221858474850390127) == None:
			await interaction.response.defer()
		else:
			author = self.author
			name = self.name
			age = self.age
			reason = self.reason
			rate = self.rate
			await interaction.response.send_modal(DeclineReason(author, name, age, reason, rate))


class ClanModal(disnake.ui.Modal):
	def __init__(self, arg):
		self.arg = arg
		components = [
			disnake.ui.TextInput(label="Ваше имя", placeholder="Дмитрий", custom_id="name", min_length=1, max_length=15),
			disnake.ui.TextInput(label="Ваш возраст", placeholder="15", custom_id="age", min_length=1, max_length=15),
			disnake.ui.TextInput(label="На что вы способны", placeholder="Ваш вариант", custom_id="reason", min_length=1, max_length=15),
			disnake.ui.TextInput(label="Оценка ваших способностей", placeholder="xx/10", custom_id="rate", min_length=1, max_length=15)
		]
		super().__init__(title="Набор в клан", components=components, custom_id="clanmodal")\

	async def callback(self, interaction: disnake.ModalInteraction) -> None:
		name = interaction.text_values["name"]
		age = interaction.text_values["age"]
		reason = interaction.text_values["reason"]
		rate = interaction.text_values["rate"]
		await interaction.response.send_message(f"Заявка отправлена администрации", ephemeral=True)
#канал с заявками
		channel = interaction.guild.get_channel(1224047385190072361)
		view = ClanButtons(interaction.author, name, age, reason, rate)

		clan_mention = interaction.guild.get_role(1221858474850390127).mention

		embed = disnake.Embed(title=f"Заявка в клан")
		embed.set_thumbnail(url=f'{interaction.author.display_avatar.url}')
		embed.add_field(name=f"**Подал:**", value=f"{interaction.author.mention}", inline=False)
		embed.add_field(name=f"**Имя:**", value=f"```{name}```", inline=False)
		embed.add_field(name=f"**Возраст:**", value=f"```{age}```", inline=False)
		embed.add_field(name=f"**Умения:**", value=f"```{reason}```", inline=False)
		embed.add_field(name=f"**Оценка умений:**", value=f"```{rate}```", inline=False)
		embed.set_image(url=f"https://cdn.discordapp.com/attachments/1211275021713014854/1224093847890559099/image_10.png?ex=661c3d3b&is=6609c83b&hm=e0207f3964274b2a842c457a9d68f27c46db1f2b012d266d7e2bf9a547a1e250&")
		await channel.send(f"{clan_mention}")
		await channel.send(embed=embed, view=view)






class ClanSelect(disnake.ui.Select):
	def __init__(self):
		options = [
			disnake.SelectOption(label="Clan", value="clan", description="Заявка в клан")
		]
		super().__init__(
			placeholder="Нажми...", options=options, min_values=0, max_values=1, custom_id="clan"
		)

	async def callback(self, interaction: disnake.MessageInteraction):
		if not interaction.values:
			await interaction.response.defer()
		else:
			await interaction.response.send_modal(ClanModal(interaction.values[0]))



class Clan_Invite(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.persistents_views_added = False

	@commands.command()
	async def claninvite(self, ctx):
		if ctx.author.guild_permissions.administrator == False:
			await ctx.response.defer()
		else:
			emb = disnake.Embed()
			emb.set_image(url=f"https://cdn.discordapp.com/attachments/1211275021713014854/1224093847890559099/image_10.png?ex=661c3d3b&is=6609c83b&hm=e0207f3964274b2a842c457a9d68f27c46db1f2b012d266d7e2bf9a547a1e250&")
			embed = disnake.Embed(title=f"Набор в клан {ctx.guild.name}")
			embed.description = f'* Желаешь стать участником клана Rebirth Night?\n' \
								f'* У тебя есть возможность сделать это прямо сейчас!\n\n' \
								f'> Требования:\n\n' \
								f'* Возраст: 15+\n' \
								f'* Адекватное поведение в клане.\n' \
								f'* Поставить приписку и ссылку на клан в "Обо мне"'
			embed.set_image(url=f"https://cdn.discordapp.com/attachments/1211275021713014854/1224093847890559099/image_10.png?ex=661c3d3b&is=6609c83b&hm=e0207f3964274b2a842c457a9d68f27c46db1f2b012d266d7e2bf9a547a1e250&")
			view = disnake.ui.View(timeout=None)
			view.add_item(ClanSelect())
			await ctx.send(embed=emb)
			await ctx.send(embed=embed, view=view)

	@commands.Cog.listener()
	async def on_connect(self):
		if self.persistents_views_added:
			return

		view = disnake.ui.View(timeout=None)
		view.add_item(ClanSelect())
		self.bot.add_view(view, message_id=1224115122512068680)



def setup(bot):
	bot.add_cog(Clan_Invite(bot))
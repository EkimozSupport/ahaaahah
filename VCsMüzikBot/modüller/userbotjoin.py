from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant
import asyncio
from VCsMusicBot.helpers.decorators import authorized_users_only, errors
from VCsMusicBot.services.callsmusic.callsmusic import client as USER
from VCsMusicBot.config import SUDO_USERS

@Client.on_message(filters.command(["userbotjoin"]) & ~filters.private & ~filters.bot)
@authorized_users_only
@errors
async def addchannel(client, message):
    chid = message.chat.id
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except:
        await message.reply_text(
            "<b>Önce beni grubun yöneticisi olarak ekle</b>",
        )
        return

    try:
        user = await USER.get_me()
    except:
        user.first_name = "MusicBot"

    try:
        await USER.join_chat(invitelink)
        await USER.send_message(message.chat.id, "İstediğiniz gibi buraya katıldım")
    except UserAlreadyParticipant:
        await message.reply_text(
            "<b>yardımcı zaten sohbetinizde</b>",
        )
    except Exception as e:
        print(e)
        await message.reply_text(
            f"<b>🛑 Flood Wait Hata 🛑 \n Kullanıcı {user.first_name}  userbot için katılma isteklerini nedeniyle ağır şekilde gruba katılmak emin kullanıcı grubunda yasaklı olmadığından emin olun olamazdı ."
            "\n\nVeya @GoodVibeesMusic ' i Grubunuza manuel olarak ekleyin ve tekrar deneyin</b>",
        )
        return
    await message.reply_text(
        "<b>yardımcı userbot sohbetinize katıldı</b>",
    )


@USER.on_message(filters.group & filters.command(["userbotleave"]))
@authorized_users_only
async def rem(USER, message):
    try:
        await USER.leave_chat(message.chat.id)
    except:
        await message.reply_text(
            f"<b>Kullanıcı grubunuzdan ayrılamadı! Sel bekleyişleri olabilir."
            "\n\nVeya beni Grubunuzdan manuel olarak atın</b>",
        )
        return
    
@Client.on_message(filters.command(["userbotleaveall"]))
async def bye(client, message):
    if message.from_user.id in SUDO_USERS:
        left=0
        failed=0
        lol = await message.reply("Assistant tüm sohbetlerden ayrılıyor")
        async for dialog in USER.iter_dialogs():
            try:
                await USER.leave_chat(dialog.chat.id)
                left = left+1
                await lol.edit(f"Asistan ayrılıyor... Left: {left} chats. Failed: {failed} chats.")
            except:
                failed=failed+1
                await lol.edit(f"Asistan ayrılıyor... Left: {left} chats. Failed: {failed} chats.")
            await asyncio.sleep(0.7)
        await client.send_message(message.chat.id, f"Left {left} chats. Failed {failed} chats.")
    
    
@Client.on_message(filters.command(["userbotjoinchannel","ubjoinc"]) & ~filters.private & ~filters.bot)
@authorized_users_only
@errors
async def addcchannel(client, message):
    try:
      conchat = await client.get_chat(message.chat.id)
      conid = conchat.linked_chat.id
      chid = conid
    except:
      await message.reply("Sohbet bağlantılı mı?")
      return    
    chat_id = chid
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except:
        await message.reply_text(
            "<b>Önce beni kanalınızın yöneticisi olarak ekleyin</b>",
        )
        return

    try:
        user = await USER.get_me()
    except:
        user.first_name = "MusicBot"

    try:
        await USER.join_chat(invitelink)
        await USER.send_message(message.chat.id, "İstediğiniz gibi buraya katıldım")
    except UserAlreadyParticipant:
        await message.reply_text(
            "<b>yardımcı zaten kanalınızda</b>",
        )
        return
    except Exception as e:
        print(e)
        await message.reply_text(
            f"<b>🛑 Flood Wait Hata 🛑 \n Kullanıcı {user.first_name} userbot için katılma isteklerini nedeniyle ağır şekilde kanala emin kullanıcı kanalda yasaklı olmadığından emin olun olamazdı."
            "\n\nVeya @GoodVibeesMusic ı Grubunuza manuel olarak ekleyin ve tekrar deneyin</b>",
        )
        return
    await message.reply_text(
        "<b>yardımcı userbot, kanalınıza katıldı</b>",
    )
    

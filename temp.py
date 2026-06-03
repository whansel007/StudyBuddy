#!/usr/bin/env python3
print("Launching the bot...")
import subprocess
from telegram import Update
from telegram.request import HTTPXRequest
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = "" #FILL THIS IN
USER_ID = [] #FILL THIS IN

REBOOT = "/root/reboot.sh"
LIST = "/root/list.sh"

async def isLoggedIn(update: Update):
    if update.effective_user.id in USER_ID:
        return 1

    await update.message.reply_text("<b>No.</b> \nWho da flip are u??? >_>", parse_mode="HTML")
    return 0    

async def whoIsOn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not await isLoggedIn(update):
            return

        await update.message.reply_text("Understood!👍 \n<i>Checking at the moment... 👀</i>", parse_mode="HTML")

        result = subprocess.run(["bash",LIST],
            capture_output=True,
            text=True,
            check=True)

        result = result.stdout 
        result = result.split()
        

        index = 0
        for i in range(len(result)-1, 0, -1):
            ch = result[i]
            if ch == "thread/INFO]:":
                index = i
                break
  
        result = result[index+1:]
        count = int(result[2])

        cutoff = result.index("online:")
        result = " ".join(result[:cutoff+1]) + " " + "".join(result[cutoff+1:]) 
        
        if count != 0:
            await update.message.reply_text(f"{result} ! 💥", parse_mode="HTML")
        else:
            await update.message.reply_text(f"There is nobody there at the moment 🍃", parse_mode="HTML")
            
    except Exception as e:
        print(f"There was an error: {e}")
        await update.message.reply_text(f"There was an error: {e}", parse_mode="HTML")

async def reboot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not await isLoggedIn(update):
            return

        await update.message.reply_text("Well most certainly! 🫡\n<i>Please hold 🙏</i>", parse_mode="HTML")
    
        subprocess.run(["bash",REBOOT])
        await update.message.reply_text("It is done! ☕️\n<code>You can now rejoin the server! 😁</code>", parse_mode="HTML")
        
    except Exception as e:
        print(f"There was an error: {e}")
        await update.message.reply_text(f"There was an error: {e}", parse_mode="HTML")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("<i>Salutations! 👋</i> \nYou can use /reboot to make the MC Server reboot 🔁👢\n<code>If I don't respond, please send me the message again 🙏</code>", parse_mode="HTML")

    if update.effective_user.id not in USER_ID:
        await update.message.reply_text("<b>Wait who diz?</b> \nIdk who u are yet >_>", parse_mode="HTML")
        return

request_client = HTTPXRequest(
    connection_pool_size=8,
    connect_timeout=30.0,
    read_timeout=30.0,
    write_timeout=30.0
)

app = (ApplicationBuilder()
       .token(BOT_TOKEN)
       .request(request_client)
       .build())

app.add_handler(CommandHandler("reboot",reboot))
app.add_handler(CommandHandler("start",start))
app.add_handler(CommandHandler("whoison",whoIsOn))
app.run_polling()
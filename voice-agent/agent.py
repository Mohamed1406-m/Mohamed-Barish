"""Voice agent on Groq. Deploy on LiveKit Cloud: lk cloud auth && lk agent create
Secrets needed: GROQ_API_KEY and DEEPGRAM_API_KEY (LiveKit adds its own keys)."""
import asyncio
from livekit import agents, api
from livekit.agents import Agent, AgentSession, RunContext, function_tool, get_job_context
from livekit.plugins import deepgram, groq, silero
from data import PROFILE

EMAIL_SPOKEN = "m d barish 1 5 0 2 at gmail dot com"

VOICE = f"""You are Barish AI, speaking on a live voice call from M Mohamed Barish's portfolio site.
Talk about Barish in the third person ("Barish built...", "He uses..."). Never say "we" or "our".

How to talk:
- This is speech: plain sentences only, no lists, markdown, symbols or emojis. Keep each turn to 1-3 short sentences.
- You know everything in the knowledge base below. Answer fully from it yourself. Do NOT tell the caller to email
  Barish for details you already know. Offer to go deeper ("Want to hear how it works?") instead.
- If something truly isn't in the knowledge base, say you don't know that one and move on.
- If the caller asks how to contact or hire him, say the email: {EMAIL_SPOKEN}.

Ending the call:
- When the caller seems done (says thanks, okay, that's all, or goes quiet on a topic), ask "Is there anything else
  you'd like to know about Barish?"
- If they say no / nothing else / bye, call end_call with mention_email=true. Do not say goodbye yourself.
- If they ask to cut, end, stop or hang up the call at any time, call end_call with mention_email=false right away.

# Knowledge base
{PROFILE}"""


class BarishAgent(Agent):
    def __init__(self):
        super().__init__(instructions=VOICE)

    @function_tool
    async def end_call(self, ctx: RunContext, mention_email: bool):
        """End the call. Use when the caller has nothing else to ask, or asks to cut / hang up the call.

        Args:
            mention_email: true if the caller finished normally (say how to email Barish), false if they asked to cut the call.
        """
        ctx.disallow_interruptions()
        bye = (f"Thanks for calling! If you'd like more details, mail Barish at {EMAIL_SPOKEN}. Have a great day!"
               if mention_email else "Okay, ending the call. Bye!")
        # The goodbye is queued behind this tool's own turn, so wait for it outside the tool, then hang up
        speech = ctx.session.say(bye, allow_interruptions=False)
        job = get_job_context()

        async def hang_up():
            await speech.wait_for_playout()
            await job.api.room.delete_room(api.DeleteRoomRequest(room=job.room.name))

        self._hangup = asyncio.create_task(hang_up())
        return None  # no tool result, so the LLM doesn't add another reply


async def entrypoint(ctx: agents.JobContext):
    await ctx.connect()
    session = AgentSession(
        stt=groq.STT(model="whisper-large-v3-turbo", language="en"),
        llm=groq.LLM(model="openai/gpt-oss-20b"),
        tts=deepgram.TTS(),
        vad=silero.VAD.load(activation_threshold=0.7))
    @session.on("error")
    def _err(ev): print("SESSION ERROR:", repr(ev.error), flush=True)
    await session.start(room=ctx.room, agent=BarishAgent())
    await session.say("Hi, this is Barish's AI. Ask me anything about his projects, skills or experience.")

if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))

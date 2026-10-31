"""Voice agent on Groq. Deploy on LiveKit Cloud: lk cloud auth && lk agent create
Secrets needed: GROQ_API_KEY and DEEPGRAM_API_KEY (LiveKit adds its own keys)."""
from livekit import agents
from livekit.agents import Agent, AgentSession
from livekit.plugins import deepgram, groq, silero
from data import SYSTEM

async def entrypoint(ctx: agents.JobContext):
    await ctx.connect()
    session = AgentSession(
        stt=groq.STT(model="whisper-large-v3-turbo", language="en"),
        llm=groq.LLM(model="llama-3.3-70b-versatile"),
        tts=deepgram.TTS(),
        vad=silero.VAD.load(activation_threshold=0.7))
    @session.on("error")
    def _err(ev): print("SESSION ERROR:", repr(ev.error), flush=True)
    await session.start(room=ctx.room, agent=Agent(instructions=SYSTEM + "\nYou are on a phone call: reply in 1-2 short sentences."))
    await session.say("Hi, this is Barish's AI. Ask me about his projects or experience.")

if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))

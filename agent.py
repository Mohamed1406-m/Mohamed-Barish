"""Voice agent worker. Vercel can't run long-lived workers: deploy this on LiveKit Cloud, Render or Railway.
Run: python agent.py dev   (needs livekit-agents, livekit-plugins-openai, livekit-plugins-silero)"""
from livekit import agents
from livekit.agents import Agent, AgentSession
from livekit.plugins import openai, silero
from portfolio.data import SYSTEM

async def entrypoint(ctx: agents.JobContext):
    await ctx.connect()
    session = AgentSession(stt=openai.STT(), llm=openai.LLM(model="gpt-4o-mini"), tts=openai.TTS(), vad=silero.VAD.load())
    await session.start(room=ctx.room, agent=Agent(instructions=SYSTEM + "\nYou are on a phone call: keep replies to 1-2 short sentences."))
    await session.say("Hi, this is Barish's AI. Ask me about his projects or experience.")

if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fn=entrypoint))

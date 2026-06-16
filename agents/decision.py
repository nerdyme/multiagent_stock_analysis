class DecisionAgent:

    def __init__(self):
        pass

    def run(self, agent_outputs):

        votes = {
            "BUY": 0,
            "HOLD": 0,
            "SELL": 0
        }

        all_reasons = []

        for result in agent_outputs:

            votes[result["vote"]] += 1

            all_reasons.extend(
                result["reason"]
            )

        final_vote = max(
            votes,
            key=votes.get
        )

        avg_confidence = int(
            sum(
                x["confidence"]
                for x in agent_outputs
            ) / len(agent_outputs)
        )

        return {
            "decision": final_vote,
            "confidence": avg_confidence,
            "reasons": all_reasons[:5]
        }
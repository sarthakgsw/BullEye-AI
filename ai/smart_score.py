def smart_score(ai_score, weighted_score):
    """
    Combines AI Score and Weighted Score
    into one Final Smart AI Score.
    """

    final_score = round((ai_score * 0.6) + (weighted_score * 0.4))

    return final_score
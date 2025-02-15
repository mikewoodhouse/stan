from app.types import Performance


class Career:
    @classmethod
    def summary(cls, player_id: int) -> Performance:
        perfs = Performance.for_player(player_id)
        highest = max(perf.highest for perf in perfs)
        highestnotout = max(perf.highestnotout for perf in perfs if perf.highest == highest)
        runsscored = sum(perf.runsscored for perf in perfs)
        innings = sum(perf.innings for perf in perfs)
        notout = sum(perf.notout for perf in perfs)
        return Performance(
            year=0,
            player_id=player_id,
            code="",
            matches=sum(perf.matches for perf in perfs),
            innings=innings,
            notout=notout,
            highest=highest,
            highestnotout=highestnotout,
            runsscored=runsscored,
            fifties=sum(perf.fifties for perf in perfs),
            hundreds=sum(perf.hundreds for perf in perfs),
            fours=sum(perf.fours for perf in perfs),
            sixes=sum(perf.sixes for perf in perfs),
        )

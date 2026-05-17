from yoinked.rules.router import Router
from yoinked.core.mover import Mover
from yoinked.core.logger import Logger


class Engine:
    def __init__(self, router: Router, mover: Mover, logger: Logger):
        self.router = router
        self.mover = mover
        self.logger = logger

    def process_file(self, file_name: str):
        decision = self.router.get_destination(file_name)

        result = self.mover.move(file_name, decision["destination"])

        self.logger.log({
            "type": "sort",
            "action": "move",
            "file": file_name,
            "source": "Downloads",
            "destination": decision["destination"],
            "status": result["success"],
            "rule": decision["rule"],
            "match": decision["match"]
        })

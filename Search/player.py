#!/usr/bin/env python3
import random

from fishing_game_core.game_tree import Node
from fishing_game_core.player_utils import PlayerController
from fishing_game_core.shared import ACTION_TO_STR


class PlayerControllerHuman(PlayerController):
    def player_loop(self):
        """
        Function that generates the loop of the game. In each iteration
        the human plays through the keyboard and send
        this to the game through the sender. Then it receives an
        update of the game through receiver, with this it computes the
        next movement.
        :return:
        """

        while True:
            # send message to game that you are ready
            msg = self.receiver()
            if msg["game_over"]:
                return


class PlayerControllerMinimax(PlayerController):

    def __init__(self):
        super(PlayerControllerMinimax, self).__init__()

    def player_loop(self):
        """
        Main loop for the minimax next move search.
        :return:
        """

        # Generate first message (Do not remove this line!)
        first_msg = self.receiver()

        while True:
            msg = self.receiver()

            # Create the root node of the game tree
            node = Node(message=msg, player=0)

            # Possible next moves: "stay", "left", "right", "up", "down"
            best_move = self.search_best_next_move(initial_tree_node=node)

            # Execute next action
            self.sender({"action": best_move, "search_time": None})

    def search_best_next_move(self, initial_tree_node):
        """
        Use minimax (and extensions) to find the best possible next move for player 0 (green boat)
        :param initial_tree_node: Initial game tree node
        :type initial_tree_node: game_tree.Node
            (see the Node class in game_tree.py for more information!)
        :return: either "stay", "left", "right", "up" or "down"
        :rtype: str
        """

        # EDIT THIS METHOD TO RETURN BEST NEXT POSSIBLE MODE USING MINIMAX ###

        # NOTE: Don't forget to initialize the children of the current node
        #       with its compute_and_get_children() method!

        children = initial_tree_node.compute_and_get_children()
        scores = []
        for child in children:
            scores.append(self.alphabeta(
                child, 2, float("-inf"), float("inf"), 1))

        best_move = children[scores.index(max(scores))].move

        return ACTION_TO_STR[best_move]

    def alphabeta(self, node, depth, alpha, beta, player):
        """
        Alpha beta pruning algorithm for the game
        :param node: the current node
        :param depth: depth maximum to go down the tree
        :param alpha: the current best value achievable by 0
        :param beta: the current best value achievable by 1
        :param player: current player
        :return: the minimax value of the state
        """
        key = self.hashkey(node)

        children = node.compute_and_get_children()
        children.sort(key=self.heuristic, reverse=True)

        if depth == 0 or len(children) == 0:
            value = self.heuristic(node)

        elif player == 0:
            value = float("-inf")
            for child in children:
                value = max(value, self.alphabeta(
                    child, depth-1, alpha, beta, 1 - player))
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
        else:
            value = float("inf")
            for child in children:
                value = min(value, self.alphabeta(
                    child, depth-1, alpha, beta, 1 - player))
                beta = min(beta, value)
                if alpha >= beta:
                    break

        visited.update({key: (depth, value)})
        return value

    # TODO: Implémenter la fonction heuristics (voir énoncé), implémenter des fonctionnalités iterative deepening search or move ordering, repeated states checking

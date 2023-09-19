#!/usr/bin/env python3
import random

from fishing_game_core.game_tree import Node
from fishing_game_core.player_utils import PlayerController
from fishing_game_core.shared import ACTION_TO_STR

import numpy as np
import time


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

        """
        children = initial_tree_node.compute_and_get_children()
        scores = []
        for child in children:
            scores.append(self.alphabeta(
                child, 2, float("-inf"), float("inf"), 1))

        best_move = children[scores.index(max(scores))].move
        """
        initial_time = time.time()

        return ACTION_TO_STR[self.iterative_deepening_search(initial_tree_node, initial_time)]
    
    def alphabeta(self, node, depth, alpha, beta, player, initial_time, visited):
        """
        Alpha beta pruning algorithm for the game
        :param node: the current node
        :param depth: depth maximum to go down the tree
        :param alpha: the current best value achievable by 0
        :param beta: the current best value achievable by 1
        :param player: current player
        :param initial_time: the time at the beginning of the search
        :param visited: the visited nodes
        :return: the minimax value of the state
        """

        k = self.compute_hash(node)
        if k in visited and visited[k][0] >= depth:
            return visited[k][1]
        
        children = node.compute_and_get_children()
        children.sort(key=self.heuristic, reverse=True)

        if time.time() - initial_time > 0.055:
            raise TimeoutError
        
        if depth == 0 or len(children) == 0:
            value = self.heuristic(node)

        elif player == 0:
            value = float("-inf")
            for child in children:
                value = max(value, self.alphabeta(
                    child, depth-1, alpha, beta, 1 - player, initial_time, visited))
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
        else:
            value = float("inf")
            for child in children:
                value = min(value, self.alphabeta(
                    child, depth-1, alpha, beta, 1 - player, initial_time, visited))
                beta = min(beta, value)
                if alpha >= beta:
                    break
        
        key = self.compute_hash(node)
        visited.update({key: (depth, value)})
        return value

    def compute_hash(self, node):
        """
        Compute the hash of the node
        :param node: the node to hash
        :return: the hash of the node
        """
        position_fish = []
        position_hook = []
        player_scores = []
        for element in node.state.hook_positions.items():
            position_hook.append(element)

        for element in node.state.get_fish_positions().items():
            position_fish.append(element)

        for element in node.state.player_scores.items():
            player_scores.append(element)

        return hash((tuple(position_hook), tuple(position_fish), tuple(player_scores)))
    
    def heuristic(self, node):
        """
        Compute the heuristic of the node
        :param node: the node to compute the heuristic
        :return: the heuristic of the node
        """

        score_diff = node.state.player_scores[0] - node.state.player_scores[1]

        estimation = 0
        for fish in node.state.fish_positions:
            distance = self.distance_from_catch(
                node.state.fish_positions[fish], node.state.hook_positions[0])
            if distance == 0 and node.state.fish_scores[fish] > 0:
                return float("inf")
            estimation = max(
                estimation, node.state.fish_scores[fish] * np.exp(-distance/10))
        return score_diff + estimation

    def distance_from_catch(self, fish_pos, hook_pos):
        """
        Compute the distance between the fish and the hook using Manhattan distance because we can only move in 4 directions
        :param fish_pos: the position of the fish
        :param hook_pos: the position of the hook
        :return: the distance between the fish and the hook
        """
        x = abs(fish_pos[0] - hook_pos[0])
        return min(x, 20 - x) + abs(fish_pos[1] - hook_pos[1])
    
    def iterative_deepening_search(self, node, initial_time):
        """
        Iterative deepening search algorithm
        :param node: the current node
        :param initial_time: the time at the beginning of the search
        :param visited: the visited nodes
        :return: the best move
        """

        
        depth = 1
        best_move = 0
        visited = {}
        while True:
            try:
                children = node.compute_and_get_children()
                scores = []
                for child in children:
                    scores.append(self.alphabeta(
                        child, depth, float("-inf"), float("inf"), 1, initial_time, visited))
                best_move = children[scores.index(max(scores))].move
                depth += 1
            except TimeoutError:
                break
        
        return best_move

    # TODO: ça sert à rien de choper un poisson choper par l'adversaire, améliorer l'heuristique



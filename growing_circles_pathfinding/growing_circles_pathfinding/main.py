## main.py

import sys
from typing import List, Tuple
import numpy as np


class TestCase:
    """Data structure for a single test case."""

    def __init__(
        self,
        n: int,
        circles: List[Tuple[int, int]],
        start: Tuple[int, int],
        goal: Tuple[int, int],
    ):
        self.n: int = n
        self.circles: List[Tuple[int, int]] = circles
        self.start: Tuple[int, int] = start
        self.goal: Tuple[int, int] = goal


class InputParser:
    """Parses input and returns a list of TestCase objects."""

    @staticmethod
    def parse() -> List[TestCase]:
        lines = []
        for line in sys.stdin:
            if line.strip() == "":
                continue
            lines.append(line.strip())
        idx = 0
        t = int(lines[idx])
        idx += 1
        test_cases: List[TestCase] = []
        for _ in range(t):
            n = int(lines[idx])
            idx += 1
            circles: List[Tuple[int, int]] = []
            for _ in range(n):
                x, y = map(int, lines[idx].split())
                circles.append((x, y))
                idx += 1
            x_s, y_s, x_t, y_t = map(int, lines[idx].split())
            idx += 1
            start = (x_s, y_s)
            goal = (x_t, y_t)
            test_cases.append(TestCase(n, circles, start, goal))
        return test_cases


class PathChecker:
    """Checks if the straight path from start to goal avoids all growing circles."""

    @staticmethod
    def check_path(test_case: TestCase) -> bool:
        start = np.array(test_case.start, dtype=np.float64)
        goal = np.array(test_case.goal, dtype=np.float64)
        direction = goal - start
        distance = np.linalg.norm(direction)
        if distance == 0:
            # Start and goal are the same point; check if inside any circle at t=0
            for circle in test_case.circles:
                center = np.array(circle, dtype=np.float64)
                if np.linalg.norm(start - center) <= 0:
                    return False
            return True

        for circle in test_case.circles:
            if PathChecker._is_touching(circle, start, goal, distance):
                return False
        return True

    @staticmethod
    def _point_to_segment_distance(
        px: float, py: float, x1: float, y1: float, x2: float, y2: float
    ) -> float:
        """Returns the minimum distance from point (px, py) to segment (x1, y1)-(x2, y2)."""
        p = np.array([px, py], dtype=np.float64)
        a = np.array([x1, y1], dtype=np.float64)
        b = np.array([x2, y2], dtype=np.float64)
        ab = b - a
        ap = p - a
        ab_len2 = np.dot(ab, ab)
        if ab_len2 == 0:
            return np.linalg.norm(ap)
        t = np.clip(np.dot(ap, ab) / ab_len2, 0.0, 1.0)
        closest = a + t * ab
        return np.linalg.norm(p - closest)

    @staticmethod
    def _is_touching(
        circle: Tuple[int, int],
        start: np.ndarray,
        goal: np.ndarray,
        distance: float,
    ) -> bool:
        """
        Returns True if the path from start to goal touches or crosses the growing circle.
        The user's position at time t is start + (goal - start) * (t / D), t in [0, D].
        The circle at (cx, cy) has radius t at time t.
        We need to check if at any t in [0, D], the distance from the user's position to the circle center is <= t.
        """
        cx, cy = circle
        sx, sy = start
        gx, gy = goal
        dx = gx - sx
        dy = gy - sy

        # Let t in [0, distance]
        # User's position at time t: (sx + dx * (t / distance), sy + dy * (t / distance))
        # Distance to circle center: sqrt((sx + dx * (t / distance) - cx)^2 + (sy + dy * (t / distance) - cy)^2)
        # Want to check if for any t in [0, distance]:
        #     sqrt((sx + dx * (t / distance) - cx)^2 + (sy + dy * (t / distance) - cy)^2) <= t
        # Square both sides (safe since t >= 0):
        #     (sx + dx * (t / distance) - cx)^2 + (sy + dy * (t / distance) - cy)^2 <= t^2
        # Rearranged as a quadratic in t:
        # Let u = t / distance, t = u * distance, u in [0, 1]
        # Position: (sx + dx * u, sy + dy * u)
        # Distance squared to center: ((sx + dx * u - cx)^2 + (sy + dy * u - cy)^2) <= (u * distance)^2

        # Let us write the quadratic in t:
        # Let t in [0, distance]
        # Let A = (dx^2 + dy^2) / distance^2 - 1 = 1 - 1 = 0 (since dx^2 + dy^2 = distance^2)
        # But let's expand:
        # (sx + dx * (t / distance) - cx)^2 + (sy + dy * (t / distance) - cy)^2 - t^2 <= 0
        # Let X = sx - cx, Y = sy - cy
        # (X + dx * (t / distance))^2 + (Y + dy * (t / distance))^2 - t^2 <= 0
        # = (X^2 + 2*X*dx*(t/distance) + dx^2*(t^2/distance^2)) +
        #   (Y^2 + 2*Y*dy*(t/distance) + dy^2*(t^2/distance^2)) - t^2
        # = (X^2 + Y^2) + 2*(X*dx + Y*dy)*(t/distance) + (dx^2 + dy^2)*(t^2/distance^2) - t^2
        # But dx^2 + dy^2 = distance^2, so:
        # = (X^2 + Y^2) + 2*(X*dx + Y*dy)*(t/distance) + distance^2*(t^2/distance^2) - t^2
        # = (X^2 + Y^2) + 2*(X*dx + Y*dy)*(t/distance) + t^2 - t^2
        # = (X^2 + Y^2) + 2*(X*dx + Y*dy)*(t/distance)
        # So the quadratic term cancels! The expression is linear in t.

        # So, the condition reduces to:
        # (X^2 + Y^2) + 2*(X*dx + Y*dy)*(t/distance) <= 0, for t in [0, distance]
        # Let C = X^2 + Y^2
        # Let B = 2*(X*dx + Y*dy)/distance
        # So, C + B*t <= 0, t in [0, distance]
        # Solve for t: t >= (-C)/B if B > 0, t <= (-C)/B if B < 0

        X = sx - cx
        Y = sy - cy
        C = X * X + Y * Y
        B = 2.0 * (X * dx + Y * dy) / distance if distance != 0 else 0.0

        # We need to check if there exists t in [0, distance] such that C + B*t <= 0
        # That is, the path touches or enters the circle at some t in [0, distance]
        # Since the path must not touch, we must return True if such t exists

        if B == 0:
            # C + B*t = C, so if C <= 0, the path starts inside or on the circle at t=0
            if C <= 0:
                return True
            else:
                return False
        else:
            t_cross = -C / B
            if B > 0:
                # C + B*t decreases as t increases
                t_start = max(0.0, t_cross)
                t_end = distance
            else:
                # C + B*t increases as t increases
                t_start = 0.0
                t_end = min(distance, t_cross)
            # Check if there is any t in [0, distance] such that C + B*t <= 0
            # That is, t_cross in [0, distance]
            if B > 0:
                if t_cross <= distance and t_cross >= 0:
                    return True
                elif C <= 0:
                    # At t=0, already inside or on the circle
                    return True
                else:
                    return False
            else:
                if t_cross >= 0 and t_cross <= distance:
                    return True
                elif C <= 0:
                    return True
                else:
                    return False


class OutputFormatter:
    """Formats and prints results for each test case."""

    @staticmethod
    def format(results: List[bool]) -> None:
        for res in results:
            print("YES" if res else "NO")


class Main:
    """Main program class."""

    @staticmethod
    def run() -> None:
        test_cases = InputParser.parse()
        results: List[bool] = []
        for test_case in test_cases:
            result = PathChecker.check_path(test_case)
            results.append(result)
        OutputFormatter.format(results)


if __name__ == "__main__":
    Main.run()

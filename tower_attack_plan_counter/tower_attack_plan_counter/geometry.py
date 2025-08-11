## geometry.py

"""
Geometry module providing geometric predicates and operations for attack plan computation.

Implements the Geometry class with methods:
- is_in_circle: Check if a point lies inside the circumcircle of three other points.
- is_in_triangle: Check if a point lies inside the triangle formed by three points.
- circumcircle: Compute the center and radius of the circumcircle of three points.
- area: Compute the area of a triangle formed by three points.

Dependencies:
    - numpy (for vectorized and robust geometric calculations)
"""

from typing import Tuple
import numpy as np


class Geometry:
    """Geometric utility class for 2D point operations."""

    @staticmethod
    def area(a: Tuple[float, float], b: Tuple[float, float], c: Tuple[float, float]) -> float:
        """Compute the signed area of triangle ABC.

        Args:
            a: First vertex as (x, y).
            b: Second vertex as (x, y).
            c: Third vertex as (x, y).

        Returns:
            The signed area (positive if ABC is counterclockwise).
        """
        ax, ay = a
        bx, by = b
        cx, cy = c
        return 0.5 * ((bx - ax) * (cy - ay) - (cx - ax) * (by - ay))

    @staticmethod
    def is_in_triangle(a: Tuple[float, float], b: Tuple[float, float], c: Tuple[float, float], p: Tuple[float, float]) -> bool:
        """Check if point p is strictly inside triangle ABC.

        Args:
            a: First vertex as (x, y).
            b: Second vertex as (x, y).
            c: Third vertex as (x, y).
            p: Point to check as (x, y).

        Returns:
            True if p is strictly inside triangle ABC, False otherwise.
        """
        # Compute areas
        area_abc = Geometry.area(a, b, c)
        if abs(area_abc) < 1e-10:
            return False  # Degenerate triangle

        area_pab = Geometry.area(p, a, b)
        area_pbc = Geometry.area(p, b, c)
        area_pca = Geometry.area(p, c, a)

        # All areas must have the same sign and none should be zero (strictly inside)
        sign = np.sign(area_abc)
        return (
            np.sign(area_pab) == sign and
            np.sign(area_pbc) == sign and
            np.sign(area_pca) == sign and
            abs(area_pab) > 1e-10 and
            abs(area_pbc) > 1e-10 and
            abs(area_pca) > 1e-10
        )

    @staticmethod
    def circumcircle(a: Tuple[float, float], b: Tuple[float, float], c: Tuple[float, float]) -> Tuple[Tuple[float, float], float]:
        """Compute the center and radius of the circumcircle of triangle ABC.

        Args:
            a: First vertex as (x, y).
            b: Second vertex as (x, y).
            c: Third vertex as (x, y).

        Returns:
            (center, radius): center as (x, y), radius as float.

        Raises:
            ValueError: If the points are colinear (no unique circumcircle).
        """
        ax, ay = a
        bx, by = b
        cx, cy = c

        # Calculate the perpendicular bisectors of AB and AC
        d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
        if abs(d) < 1e-10:
            raise ValueError("Points are colinear; circumcircle is undefined.")

        ux = (
            ((ax ** 2 + ay ** 2) * (by - cy) +
             (bx ** 2 + by ** 2) * (cy - ay) +
             (cx ** 2 + cy ** 2) * (ay - by)) / d
        )
        uy = (
            ((ax ** 2 + ay ** 2) * (cx - bx) +
             (bx ** 2 + by ** 2) * (ax - cx) +
             (cx ** 2 + cy ** 2) * (bx - ax)) / d
        )
        center = (ux, uy)
        radius = np.hypot(ux - ax, uy - ay)
        return center, radius

    @staticmethod
    def is_in_circle(a: Tuple[float, float], b: Tuple[float, float], c: Tuple[float, float], p: Tuple[float, float]) -> bool:
        """Check if point p is strictly inside the circumcircle of triangle ABC.

        Args:
            a: First vertex as (x, y).
            b: Second vertex as (x, y).
            c: Third vertex as (x, y).
            p: Point to check as (x, y).

        Returns:
            True if p is strictly inside the circumcircle, False otherwise.
        """
        try:
            center, radius = Geometry.circumcircle(a, b, c)
        except ValueError:
            return False  # Colinear points, no valid circumcircle

        px, py = p
        cx, cy = center
        dist = np.hypot(px - cx, py - cy)
        # Strictly inside: distance < radius - epsilon
        return dist < radius - 1e-10


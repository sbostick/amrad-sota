#!/usr/bin/env python
from attrs import define, field
from typing import Tuple


@define(frozen=True)
class Coords:
    """
    Represents a geographical coordinate pair with multiple initialization methods
    and conversion capabilities to/from Maidenhead grid locators.

    Internal representation uses decimal degrees where:
    - Latitude ranges from -90 to +90 (negative for South)
    - Longitude ranges from -180 to +180 (negative for West)
    """
    lat: float = field()
    lon: float = field()

    @classmethod
    def from_dec_degrees(cls, lat: float, lon: float) -> 'Coords':
        """
        Create Coords from decimal degrees.

        Args:
            lat: Latitude in decimal degrees (-90 to +90)
            lon: Longitude in decimal degrees (-180 to +180)
        """
        if not -90 <= lat <= 90:
            raise ValueError("Latitude must be between -90 and +90 degrees")
        if not -180 <= lon <= 180:
            raise ValueError("Longitude must be between -180 and +180 degrees")
        return cls(lat=lat, lon=lon)

    @classmethod
    def from_deg_min_sec(
        cls,
        lat_deg: float,
        lat_min: float,
        lat_sec: float,
        lon_deg: float,
        lon_min: float,
        lon_sec: float,
        lat_hemisphere: str = 'N',
        lon_hemisphere: str = 'W'
    ) -> 'Coords':
        """
        Create Coords from degrees, minutes, and seconds.

        Args:
            lat_deg: Latitude degrees (0 to 90)
            lat_min: Latitude minutes (0 to 60)
            lat_sec: Latitude seconds (0 to 60)
            lon_deg: Longitude degrees (0 to 180)
            lon_min: Longitude minutes (0 to 60)
            lon_sec: Longitude seconds (0 to 60)
            lat_hemisphere: 'N' or 'S'
            lon_hemisphere: 'E' or 'W'
        """
        # Validate inputs
        if not all(0 <= x < 60 for x in (lat_min, lat_sec, lon_min, lon_sec)):
            raise ValueError("Minutes and seconds must be between 0 and 60")
        if not 0 <= lat_deg <= 90:
            raise ValueError("Latitude degrees must be between 0 and 90")
        if not 0 <= lon_deg <= 180:
            raise ValueError("Longitude degrees must be between 0 and 180")
        if lat_hemisphere not in ('N', 'S'):
            raise ValueError("Latitude hemisphere must be 'N' or 'S'")
        if lon_hemisphere not in ('E', 'W'):
            raise ValueError("Longitude hemisphere must be 'E' or 'W'")

        # Convert to decimal degrees
        lat = lat_deg + (lat_min / 60) + (lat_sec / 3600)
        lon = lon_deg + (lon_min / 60) + (lon_sec / 3600)

        # Apply hemispheres
        if lat_hemisphere == 'S':
            lat = -lat
        if lon_hemisphere == 'W':
            lon = -lon

        return cls(lat=lat, lon=lon)

    @classmethod
    def from_maidenhead(cls, grid: str) -> 'Coords':
        """
        Create Coords from a Maidenhead grid locator string.

        Args:
            grid: Maidenhead grid locator (2-8 characters)
        """
        grid = grid.upper()
        if not 2 <= len(grid) <= 8 or len(grid) % 2 != 0:
            raise ValueError("Grid must be 2, 4, 6, or 8 characters")

        lon = -180.0  # Start at origin
        lat = -90.0

        # Field (18° × 18°)
        if not ('A' <= grid[0] <= 'R' and 'A' <= grid[1] <= 'R'):
            raise ValueError("Invalid field characters")
        lon += (ord(grid[0]) - ord('A')) * 20
        lat += (ord(grid[1]) - ord('A')) * 10

        # Square (2° × 1°)
        if len(grid) >= 4:
            if not (grid[2].isdigit() and grid[3].isdigit()):
                raise ValueError("Invalid square characters")
            lon += int(grid[2]) * 2
            lat += int(grid[3])

        # Subsquare (5' × 2.5')
        if len(grid) >= 6:
            if not ('A' <= grid[4] <= 'X' and 'A' <= grid[5] <= 'X'):
                raise ValueError("Invalid subsquare characters")
            lon += (ord(grid[4]) - ord('A')) * (5/60)
            lat += (ord(grid[5]) - ord('A')) * (2.5/60)

        # Extended square (30" × 15")
        if len(grid) == 8:
            if not (grid[6].isdigit() and grid[7].isdigit()):
                raise ValueError("Invalid extended square characters")
            lon += int(grid[6]) * (30/3600)
            lat += int(grid[7]) * (15/3600)

        return cls(lat=lat, lon=lon)

    def to_deg_min_sec(self) -> Tuple[Tuple[float, float, float, str],
                                      Tuple[float, float, float, str]]:
        """
        Convert to degrees, minutes, seconds format.

        Returns:
            ((lat_deg, lat_min, lat_sec, lat_hemisphere),
             (lon_deg, lon_min, lon_sec, lon_hemisphere))
        """
        def decimal_to_dms(decimal: float, is_latitude: bool) -> Tuple[float, float, float, str]:
            hemisphere = 'N' if is_latitude else 'E'
            if decimal < 0:
                hemisphere = 'S' if is_latitude else 'W'
                decimal = abs(decimal)

            degrees = int(decimal)
            minutes_float = (decimal - degrees) * 60
            minutes = int(minutes_float)
            seconds = (minutes_float - minutes) * 60

            return (degrees, minutes, seconds, hemisphere)

        return (decimal_to_dms(self.lat, True),
                decimal_to_dms(self.lon, False))

    def to_maidenhead(self, precision: int = 4) -> str:
        """
        Convert to Maidenhead grid locator.

        Args:
            precision: Number of character pairs (1-4) for desired precision:
                      1 pair (field) = 18° × 18°
                      2 pairs (square) = 2° × 1°
                      3 pairs (subsquare) = 5' × 2.5'
                      4 pairs (extended) = 30" × 15"
        """
        if not 1 <= precision <= 4:
            raise ValueError("Precision must be between 1 and 4 character pairs")

        # Normalize longitude to 0-360° range and latitude to 0-180° range
        lon = (self.lon + 180) % 360
        lat = max(-90, min(90, self.lat)) + 90

        result = []

        # Field (18° × 18°)
        result.append(chr(ord('A') + int(lon / 20)))
        result.append(chr(ord('A') + int(lat / 10)))

        if precision >= 2:
            # Square (2° × 1°)
            result.append(str(int((lon % 20) / 2)))
            result.append(str(int(lat % 10)))

        if precision >= 3:
            # Subsquare (5' × 2.5')
            lon_rem = (lon % 2) * 60
            lat_rem = (lat % 1) * 60
            result.append(chr(ord('A') + int(lon_rem / 5)))
            result.append(chr(ord('A') + int(lat_rem / 2.5)))

        if precision >= 4:
            # Extended square (30" × 15")
            lon_rem = (lon_rem % 5) * 60
            lat_rem = (lat_rem % 2.5) * 60
            result.append(str(int(lon_rem / 30)))
            result.append(str(int(lat_rem / 15)))

        return ''.join(result)

import { Grid, Text, RangeSlider, Group, NumberInput } from "@mantine/core";

interface StatFilterProps {
  statKey: string; // e.g., "pts", "trb"
  label: string;   // e.g., "Points", "Total Rebounds"
  team1Filter: any;
  setTeam1Filter: React.Dispatch<React.SetStateAction<any>>;
  team2Filter: any;
  setTeam2Filter: React.Dispatch<React.SetStateAction<any>>;
  filterType: string;
  sliders?: boolean;
  max: number;
}

export default function StatFilter({
  statKey,
  label,
  team1Filter,
  setTeam1Filter,
  team2Filter,
  setTeam2Filter,
  filterType,
  sliders = true,
  max
}: StatFilterProps) {
  const getLabel = (team: 1 | 2) => {
    if (filterType === "home-visitor") return team === 1 ? `Home Team ${label}` : `Visiting Team ${label}`;
    if (filterType === "winner-loser") return team === 1 ? `Winning Team ${label}` : `Losing Team ${label}`;
    return `Team ${team} ${label}`;
  };

  return (
    <Grid className="filter-grid" gutter="md">
      {[1, 2].map((team) => (
        <Grid.Col key={team} span={{ base: 12, sm: 6 }}>
          <Text fw={600}>{getLabel(team as 1 | 2)}</Text>

          {sliders && (
            <RangeSlider
              minRange={0}
              max={max}
              color="blue"
              value={[
                team === 1 ? team1Filter[`${statKey}_min`] : team2Filter[`${statKey}_min`],
                team === 1 ? team1Filter[`${statKey}_max`] : team2Filter[`${statKey}_max`]
              ]}
              onChange={(value) => {
                if (team === 1) {
                  setTeam1Filter((prev) => ({
                    ...prev,
                    [`${statKey}_min`]: value[0],
                    [`${statKey}_max`]: value[1]
                  }));
                } else {
                  setTeam2Filter((prev) => ({
                    ...prev,
                    [`${statKey}_min`]: value[0],
                    [`${statKey}_max`]: value[1]
                  }));
                }
              }}
              marks={[
                { value: 0, label: "0" },
                { value: max / 2, label: String(max / 2) },
                { value: max, label: String(max) }
              ]}
            />
          )}

          <Group grow mt="xs">
            <NumberInput
              min={0}
              max={max}
              value={team === 1 ? team1Filter[`${statKey}_min`] : team2Filter[`${statKey}_min`]}
              onChange={(value) => {
                if (team === 1) {
                  setTeam1Filter((prev) => ({ ...prev, [`${statKey}_min`]: Number(value) }));
                } else {
                  setTeam2Filter((prev) => ({ ...prev, [`${statKey}_min`]: Number(value) }));
                }
              }}
              label="Min"
            />
            <NumberInput
              min={0}
              max={max}
              value={team === 1 ? team1Filter[`${statKey}_max`] : team2Filter[`${statKey}_max`]}
              onChange={(value) => {
                if (team === 1) {
                  setTeam1Filter((prev) => ({ ...prev, [`${statKey}_max`]: Number(value) }));
                } else {
                  setTeam2Filter((prev) => ({ ...prev, [`${statKey}_max`]: Number(value) }));
                }
              }}
              label="Max"
            />
          </Group>
        </Grid.Col>
      ))}
    </Grid>
  );
}

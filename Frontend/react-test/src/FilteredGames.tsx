
import React, { useState } from "react";
import {Table, Loader, Alert, NumberInput, RangeSlider, Button, Group, Container, Grid, Text} from "@mantine/core";
import { getFilteredGames, type FilterParams } from "./api";
import { Link } from "react-router-dom";

export default function FilteredGames() {
    const [games, setGames] = useState<any[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
  // Points
    const [team1Filter, setTeam1Filter] = useState<FilterParams>({
        pts_min: 0,
        pts_max: 200,
        ast_min: 0,
        ast_max: 60,
        trb_min: 0,
        trb_max: 100,
        orb_min: 0,
        orb_max: 40,
        drb_min: 0,
        drb_max: 60,
        blk_min: 0,
        blk_max: 30,
        stl_min: 0,
        stl_max: 30,
        fga_min: 0,
        fga_max: 150,
        fgm_min: 0,
        fgm_max: 80,
        fg_pct_min: 0,
        fg_pct_max: 100,
        tpa_min: 0,
        tpa_max: 80,
        tpm_min: 0,
        tpm_max: 40,
        tp_pct_min: 0,
        tp_pct_max: 100,
        fta_min: 0,
        fta_max: 80,
        ftm_min: 0,
        ftm_max: 80,
        ft_pct_min: 0,
        ft_pct_max: 100,
        fouls_min: 0,
        fouls_max: 60,
        to_min: 0,
        to_max: 40
    });
    const [team2Filter, setTeam2Filter] = useState<FilterParams>({
        pts_min: 0,
        pts_max: 200,
        ast_min: 0,
        ast_max: 60,
        trb_min: 0,
        trb_max: 100,
        orb_min: 0,
        orb_max: 40,
        drb_min: 0,
        drb_max: 60,
        blk_min: 0,
        blk_max: 30,
        stl_min: 0,
        stl_max: 30,
        fga_min: 0,
        fga_max: 150,
        fgm_min: 0,
        fgm_max: 80,
        fg_pct_min: 0,
        fg_pct_max: 100,
        tpa_min: 0,
        tpa_max: 80,
        tpm_min: 0,
        tpm_max: 40,
        tp_pct_min: 0,
        tp_pct_max: 100,
        fta_min: 0,
        fta_max: 80,
        ftm_min: 0,
        ftm_max: 80,
        ft_pct_min: 0,
        ft_pct_max: 100,
        fouls_min: 0,
        fouls_max: 60,
        to_min: 0,
        to_max: 40
    });

    const [team1Points, setTeam1Points] = useState<[number, number]>([0, 200]);
    const [team2Points, setTeam2Points] = useState<[number, number]>([0, 200]);

    // Assists
    const [team1Assists, setTeam1Assists] = useState<[number, number]>([0, 60]);
    const [team2Assists, setTeam2Assists] = useState<[number, number]>([0, 60]);

    // Total Rebounds
    const [team1TotRebounds, setTeam1TotRebounds] = useState<[number, number]>([0, 100]);
    const [team2TotRebounds, setTeam2TotRebounds] = useState<[number, number]>([0, 100]);

    // Offensive Rebounds
    const [team1OffRebounds, setTeam1OffRebounds] = useState<[number, number]>([0, 40]);
    const [team2OffRebounds, setTeam2OffRebounds] = useState<[number, number]>([0, 40]);

    // Defensive Rebounds
    const [team1DefRebounds, setTeam1DefRebounds] = useState<[number, number]>([0, 60]);
    const [team2DefRebounds, setTeam2DefRebounds] = useState<[number, number]>([0, 60]);

    // Blocks
    const [team1Blocks, setTeam1Blocks] = useState<[number, number]>([0, 30]);
    const [team2Blocks, setTeam2Blocks] = useState<[number, number]>([0, 30]);

    // Steals
    const [team1Steals, setTeam1Steals] = useState<[number, number]>([0, 30]);
    const [team2Steals, setTeam2Steals] = useState<[number, number]>([0, 30]);

    // Field Goals Attempted
    const [team1FGA, setTeam1FGA] = useState<[number, number]>([0, 150]);
    const [team2FGA, setTeam2FGA] = useState<[number, number]>([0, 150]);

    // Field Goals Made
    const [team1FGM, setTeam1FGM] = useState<[number, number]>([0, 80]);
    const [team2FGM, setTeam2FGM] = useState<[number, number]>([0, 80]);

    // Field Goal %
    const [team1FGPct, setTeam1FGPct] = useState<[number, number]>([0, 100]);
    const [team2FGPct, setTeam2FGPct] = useState<[number, number]>([0, 100]);

    // Three-Point Attempts
    const [team1TPA, setTeam1TPA] = useState<[number, number]>([0, 80]);
    const [team2TPA, setTeam2TPA] = useState<[number, number]>([0, 80]);

    // Three-Point Makes
    const [team1TPM, setTeam1TPM] = useState<[number, number]>([0, 40]);
    const [team2TPM, setTeam2TPM] = useState<[number, number]>([0, 40]);

    // Three-Point %
    const [team1TPPct, setTeam1TPPct] = useState<[number, number]>([0, 100]);
    const [team2TPPct, setTeam2TPPct] = useState<[number, number]>([0, 100]);

    // Free Throw Attempts
    const [team1FTA, setTeam1FTA] = useState<[number, number]>([0, 80]);
    const [team2FTA, setTeam2FTA] = useState<[number, number]>([0, 80]);

    // Free Throw Makes
    const [team1FTM, setTeam1FTM] = useState<[number, number]>([0, 80]);
    const [team2FTM, setTeam2FTM] = useState<[number, number]>([0, 80]);

    // Free Throw %
    const [team1FTPct, setTeam1FTPct] = useState<[number, number]>([0, 100]);
    const [team2FTPct, setTeam2FTPct] = useState<[number, number]>([0, 100]);

    // Fouls
    const [team1Fouls, setTeam1Fouls] = useState<[number, number]>([0, 60]);
    const [team2Fouls, setTeam2Fouls] = useState<[number, number]>([0, 60]);

    // Turnovers
    const [team1Turnovers, setTeam1Turnovers] = useState<[number, number]>([0, 40]);
    const [team2Turnovers, setTeam2Turnovers] = useState<[number, number]>([0, 40]);

    const [pointsFilter, setPointsFilter] = useState(true);
    const [assistsFilter, setAssistsFilter] = useState(false);
    const [totReboundsFilter, setTotReboundsFilter] = useState(false);
    const [offReboundsFilter, setOffReboundsFilter] = useState(false);
    const [filterType, setFilterType] = useState<string>("");
    const [sliders, setSliders] = useState(true);

    const setTeam1PointsMin = (value: number | string) => {
        if (typeof value === "number") setTeam1Points([value, team1Points[1]]);
    };
    const setTeam1PointsMax = (value: number | string) => {
        if (typeof value === "number") setTeam1Points([team1Points[0], value]);
    };
    const setTeam2PointsMin = (value: number | string) => {
        if (typeof value === "number") setTeam2Points([value, team2Points[1]]);
    };
    const setTeam2PointsMax = (value: number | string) => {
        if (typeof value === "number") setTeam2Points([team2Points[0], value]);
    };

    const setTeam1AssistsMin = (value: number | string) => {
        if (typeof value === "number") setTeam1Assists([value, team1Assists[1]]);
    };
    const setTeam1AssistsMax = (value: number | string) => {
        if (typeof value === "number") setTeam1Points([team1Assists[0], value]);
    };
    const setTeam2AssistsMin = (value: number | string) => {
        if (typeof value === "number") setTeam2Points([value, team2Assists[1]]);
    };
    const setTeam2AssistsMax = (value: number | string) => {
        if (typeof value === "number") setTeam2Points([team2Assists[0], value]);
    };

    // const setTeam1PointsMin = (value: number | string) => {
    //     if (typeof value === "number") setTeam1Points([value, Team1Points[1]]);
    // };
    // const setTeam1PointsMax = (value: number | string) => {
    //     if (typeof value === "number") setTeam1Points([Team1Points[0], value]);
    // };
    // const setTeam2PointsMin = (value: number | string) => {
    //     if (typeof value === "number") setTeam2Points([value, Team2Points[1]]);
    // };
    // const setTeam2PointsMax = (value: number | string) => {
    //     if (typeof value === "number") setTeam2Points([Team2Points[0], value]);
    // };

    const filter = async () => {
        // const filter1: FilterParams = {
        // pts_min: pointsFilter? team1Filter.pts_min : undefined,
        // pts_max: pointsFilter? team1Filter.pts_max: undefined,
        // };
        // const filter2: FilterParams = {
        // pts_min: pointsFilter? team2Filter.pts_min: undefined,
        // pts_max: pointsFilter? team2Filter.pts_max: undefined,
        // };
        const marginFilter = undefined;
        setLoading(true);
        getFilteredGames(team1Filter, team2Filter, filterType, marginFilter)
        .then((res) => {
            setGames(res);
            setError(null);
        })
        .catch((err) => setError(err.message))
        .finally(() => setLoading(false));
    };

    if (loading) return <Loader />;
    if (error) return <Alert color="red">{error}</Alert>;

    return (
        <Container size="xl" mt="lg">
            <Text size="xl" fw={700} mb="lg">
                Game Filters:
            </Text>
            <Button
                onClick={() => setFilterType("")}
                mt="md"
                variant={filterType === "" ? "filled" : "light"}
            >
                Normal Filter
            </Button>

            <Button
                onClick={() => setFilterType("home-visitor")}
                mt="md"
                variant={filterType === "home-visitor" ? "filled" : "light"}
            >
                Home/Visitor Filter
            </Button>

            <Button
                onClick={() => setFilterType("winner-loser")}
                mt="md"
                variant={filterType === "winner-loser" ? "filled" : "light"}
            >
                Winner/Loser Filter
            </Button>
            <h2></h2>
            <Button
                onClick={() => setSliders(!sliders)}
                mt="md"
                variant={sliders === true ? "filled" : "light"}
            >
                Include Sliders
            </Button>

            {/* Points Filters */}
            <Grid gutter="md">
                {/* Team1 Points Filter */}
                {pointsFilter && <Grid.Col span={{ base: 12, sm: 6 }}>
                <Text fw={600}>
                    {filterType === "home-visitor"
                        ? "Home Team Points"
                        : filterType === "winner-loser"
                        ? "Winning Team Points"
                        : "Team 1 Points"}
                </Text>

                {sliders &&<RangeSlider
                    minRange={0}
                    max={200}
                    color="blue"
                    value={[team1Filter.pts_min!, team1Filter.pts_max!]}
                    onChange={(value) =>
                        setTeam1Filter((prev) => ({
                            ...prev,
                            pts_min: value[0],
                            pts_max: value[1],
                        }))
                    }
                    marks={[
                    { value: 0, label: "0" },
                    { value: 100, label: "100" },
                    { value: 200, label: "200" },
                    ]}
                />}
                <Group grow mt="xs">
                    <NumberInput
                    min={0}
                    max={200}
                    value={team1Filter.pts_min}
                    onChange={(value) =>
                        setTeam1Filter((prev) => ({
                            ...prev,
                            pts_min: Number(value)
                        }))
                    }
                    label="Min"
                    />
                    <NumberInput
                    min={0}
                    max={200}
                    value={team1Filter.pts_max}
                    onChange={(value) =>
                        setTeam1Filter((prev) => ({
                            ...prev,
                            pts_max: Number(value),
                        }))
                    }
                    label="Max"
                    />
                </Group>
                </Grid.Col>}

                {/* Team2 Points Filter */}
                {pointsFilter && <Grid.Col span={{ base: 12, sm: 6 }}>
                <Text fw={600}>
                    {filterType === "home-visitor"
                        ? "Visiting Team Points"
                        : filterType === "winner-loser"
                        ? "Losing Team Points"
                        : "Team 2 Points"}
                </Text>
                {sliders && <RangeSlider
                    minRange={0}
                    max={200}
                    color="blue"
                    value={[team2Filter.pts_min!, team2Filter.pts_max!]}
                    onChange={(value) =>
                        setTeam2Filter((prev) => ({
                            ...prev,
                            pts_min: value[0],
                            pts_max: value[1],
                        }))
                    }
                    marks={[
                    { value: 0, label: "0" },
                    { value: 100, label: "100" },
                    { value: 200, label: "200" },
                    ]}
                />}
                <Group grow mt="xs">
                    <NumberInput
                    min={0}
                    max={200}
                    value={team2Filter.pts_min}
                    onChange={(value) =>
                        setTeam2Filter((prev) => ({
                            ...prev,
                            pts_min: Number(value)
                        }))
                    }
                    label="Min"
                    />
                    <NumberInput
                    min={0}
                    max={200}
                    value={team2Filter.pts_max}
                    onChange={(value) =>
                        setTeam2Filter((prev) => ({
                            ...prev,
                            pts_max: Number(value),
                        }))
                    }
                    label="Max"
                    />
                </Group>
                </Grid.Col>}
                <Button onClick={() => setPointsFilter(!pointsFilter)} mt="md">
                    {pointsFilter === true ? "Remove Points Filter" : "Add Points Filter"}
                </Button>
            </Grid>
            
            {/* Assists Filters */}
            <Grid gutter="md">
                {assistsFilter && <Grid.Col span={{ base: 12, sm: 6 }}>
                <Text fw={600}>
                    {filterType === "home-visitor"
                        ? "Home Team Assists"
                        : filterType === "winner-loser"
                        ? "Winning Team Assists"
                        : "Team 1 Assists"}
                </Text>

                {sliders &&<RangeSlider
                    minRange={0}
                    max={200}
                    color="blue"
                    value={[team1Filter.ast_min!, team1Filter.ast_max!]}
                    onChange={(value) =>
                        setTeam1Filter((prev) => ({
                            ...prev,
                            ast_min: value[0],
                            ast_max: value[1],
                        }))
                    }
                    marks={[
                    { value: 0, label: "0" },
                    { value: 100, label: "100" },
                    { value: 200, label: "200" },
                    ]}
                />}
                <Group grow mt="xs">
                    <NumberInput
                    min={0}
                    max={200}
                    value={team1Filter.ast_min}
                    onChange={(value) =>
                        setTeam1Filter((prev) => ({
                            ...prev,
                            ast_min: Number(value)
                        }))
                    }
                    label="Min"
                    />
                    <NumberInput
                    min={0}
                    max={200}
                    value={team1Filter.ast_max}
                    onChange={(value) =>
                        setTeam1Filter((prev) => ({
                            ...prev,
                            ast_max: Number(value),
                        }))
                    }
                    label="Max"
                    />
                </Group>
                </Grid.Col>}

                {assistsFilter && <Grid.Col span={{ base: 12, sm: 6 }}>
                <Text fw={600}>
                    {filterType === "home-visitor"
                        ? "Visiting Team Assists"
                        : filterType === "winner-loser"
                        ? "Losing Team Assists"
                        : "Team 2 Assists"}
                </Text>
                {sliders && <RangeSlider
                    minRange={0}
                    max={200}
                    color="blue"
                    value={[team2Filter.ast_min!, team2Filter.ast_max!]}
                    onChange={(value) =>
                        setTeam2Filter((prev) => ({
                            ...prev,
                            ast_min: value[0],
                            ast_max: value[1],
                        }))
                    }
                    marks={[
                    { value: 0, label: "0" },
                    { value: 100, label: "100" },
                    { value: 200, label: "200" },
                    ]}
                />}
                <Group grow mt="xs">
                    <NumberInput
                    min={0}
                    max={200}
                    value={team2Filter.ast_min}
                    onChange={(value) =>
                        setTeam2Filter((prev) => ({
                            ...prev,
                            ast_min: Number(value)
                        }))
                    }
                    label="Min"
                    />
                    <NumberInput
                    min={0}
                    max={200}
                    value={team2Filter.ast_max}
                    onChange={(value) =>
                        setTeam2Filter((prev) => ({
                            ...prev,
                            ast_max: Number(value),
                        }))
                    }
                    label="Max"
                    />
                </Group>
                </Grid.Col>}
                <Button onClick={() => setAssistsFilter(!assistsFilter)} mt="md">
                    {assistsFilter === true ? "Remove Assists Filter" : "Add Assists Filter"}
                </Button>
            </Grid>

            {/* Tot Rebounds Filters */}
            <Grid gutter="md">
                {totReboundsFilter && <Grid.Col span={{ base: 12, sm: 6 }}>
                <Text fw={600}>
                    {filterType === "home-visitor"
                        ? "Home Team Total Rebounds"
                        : filterType === "winner-loser"
                        ? "Winning Team Total Rebounds"
                        : "Team 1 Total Rebounds"}
                </Text>

                {sliders &&<RangeSlider
                    minRange={0}
                    max={200}
                    color="blue"
                    value={[team1Filter.ast_min!, team1Filter.ast_max!]}
                    onChange={(value) =>
                        setTeam1Filter((prev) => ({
                            ...prev,
                            ast_min: value[0],
                            ast_max: value[1],
                        }))
                    }
                    marks={[
                    { value: 0, label: "0" },
                    { value: 100, label: "100" },
                    { value: 200, label: "200" },
                    ]}
                />}
                <Group grow mt="xs">
                    <NumberInput
                    min={0}
                    max={200}
                    value={team1Filter.trb_min}
                    onChange={(value) =>
                        setTeam1Filter((prev) => ({
                            ...prev,
                            trb_min: Number(value)
                        }))
                    }
                    label="Min"
                    />
                    <NumberInput
                    min={0}
                    max={200}
                    value={team1Filter.trb_max}
                    onChange={(value) =>
                        setTeam1Filter((prev) => ({
                            ...prev,
                            trb_max: Number(value),
                        }))
                    }
                    label="Max"
                    />
                </Group>
                </Grid.Col>}

                {totReboundsFilter && <Grid.Col span={{ base: 12, sm: 6 }}>
                <Text fw={600}>
                    {filterType === "home-visitor"
                        ? "Visiting Team Points"
                        : filterType === "winner-loser"
                        ? "Losing Team Points"
                        : "Team 2 Points"}
                </Text>
                {sliders && <RangeSlider
                    minRange={0}
                    max={200}
                    color="blue"
                    value={[team2Filter.trb_min!, team2Filter.trb_max!]}
                    onChange={(value) =>
                        setTeam2Filter((prev) => ({
                            ...prev,
                            trb_min: value[0],
                            trb_max: value[1],
                        }))
                    }
                    marks={[
                    { value: 0, label: "0" },
                    { value: 100, label: "100" },
                    { value: 200, label: "200" },
                    ]}
                />}
                <Group grow mt="xs">
                    <NumberInput
                    min={0}
                    max={200}
                    value={team2Filter.trb_min}
                    onChange={(value) =>
                        setTeam2Filter((prev) => ({
                            ...prev,
                            trb_min: Number(value)
                        }))
                    }
                    label="Min"
                    />
                    <NumberInput
                    min={0}
                    max={200}
                    value={team2Filter.trb_max}
                    onChange={(value) =>
                        setTeam2Filter((prev) => ({
                            ...prev,
                            trb_max: Number(value),
                        }))
                    }
                    label="Max"
                    />
                </Group>
                </Grid.Col>}
                <Button onClick={() => setTotReboundsFilter(!totReboundsFilter)} mt="md">
                    {totReboundsFilter === true ? "Remove Total Rebounds Filter" : "Add Total Rebounds Filter"}
                </Button>
            </Grid>
                    
            <Button onClick={filter} mt="md">
                Filter
            </Button>

            <Text size="lg" fw={700} mt="xl" mb="sm">
                Filtered Games
            </Text>

            {/* Full width table */}
            {games.length > 0 && <Table striped highlightOnHover withTableBorder style={{ width: "100%" }}>
                <thead>
                <tr>
                    <th>Date</th>
                    <th>Visitor Team</th>
                    <th>Home Team</th>
                    <th></th>
                </tr>
                </thead>
                <tbody>
                {games.map((game) => (
                    <tr key={game["Game ID"]}>
                    <td>{game["Date"]}</td>
                    <td>
                        {game["Visitor Team"]}
                    </td>
                    <td>{game["Home Team"]}</td>
                    <td>
                        <Link to={`/game/${game["Game ID"]}`} target="_blank" rel="noopener noreferrer">
                            Box Score
                        </Link>
                    </td>
                    </tr>
                ))}
                </tbody>
            </Table>}
        </Container>
    );
}

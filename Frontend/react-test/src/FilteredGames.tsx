
import React, { useState } from "react";
import {Table, Loader, Alert, NumberInput, RangeSlider, Button, Group, Container, Grid, Text, Card, Checkbox, Stack} from "@mantine/core";
import StatFilter from "./StatFilter";
import { getFilteredGames, type FilterParams } from "./api";
import { Link } from "react-router-dom";
import './App.css';

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

    const [filterType, setFilterType] = useState<string>("");
    const [sliders, setSliders] = useState(true);
    const [activeFilters, setActiveFilters] = useState<string[]>(['points']);



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
            <Card withBorder padding="md" mb="lg">
                <Text fw={600} mb="xs">Active Filters</Text>
                <Checkbox.Group
                    value={activeFilters}
                    onChange={setActiveFilters}
                >
                    <Group align="flex-start" gap="xl"> 
                        <Stack>
                            <Checkbox value="points" label="Points" />
                            <Checkbox value="tot rebounds" label="Total Rebounds" />
                            <Checkbox value="off rebounds" label="Offensive Rebounds" />
                            <Checkbox value="def rebounds" label="Defensive Rebounds" />
                        </Stack>
                        <Stack>
                            <Checkbox value="assists" label="Assists" />
                            <Checkbox value="steals" label="Steals" />
                            <Checkbox value="blocks" label="Blocks" />
                            <Checkbox value="turnovers" label="Turnovers" />
                        </Stack>
                        <Stack>
                            <Checkbox value="fga" label="Field Goal Attempts" />
                            <Checkbox value="fgm" label="Field Goals Made" />
                            <Checkbox value="fg%" label="Field Goal %" />
                            <Checkbox value="fouls" label="Fouls" />
                        </Stack>
                        <Stack>
                            <Checkbox value="fta" label="Free Throw Attempts" />
                            <Checkbox value="ftm" label="Free Throws Made" />
                            <Checkbox value="ft%" label="Free Throw %" />
                        </Stack>
                        <Stack>
                            <Checkbox value="3pa" label="3 Point Attempts" />
                            <Checkbox value="3pm" label="3 Pointers Made" />
                            <Checkbox value="3p%" label="3 Point %" />
                        </Stack>
                    </Group>
                </Checkbox.Group>
            </Card>

            {activeFilters.length > 0 &&<Button
                onClick={() => setSliders(!sliders)}
                mt="md"
                variant={!sliders ? "filled" : "light"}
            >
                {sliders ? "Remove Sliders" : "Add Sliders"}
            </Button>}
            

            {/* Points Filters */}
            {activeFilters.includes("points") && <Grid className="filter-grid" gutter="md">
                {/* Team1 Points Filter */}
                <Grid.Col span={{ base: 12, sm: 6 }}>
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
                </Grid.Col>
                
                {/* Team2 Points Filter */}
                <Grid.Col span={{ base: 12, sm: 6 }}>
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
                </Grid.Col>
                {/* <Button onClick={() => setPointsFilter(!pointsFilter)} mt="md" variant={!pointsFilter ? "filled" : "light"}>
                    {pointsFilter ? "Remove Points Filter" : "Add Points Filter"}
                </Button> */}
            </Grid>}

            {/* Tot Rebounds Filters */}
            {activeFilters.includes("tot rebounds") && <Grid className="filter-grid" gutter="md">
                <Grid.Col span={{ base: 12, sm: 6 }}>
                <Text fw={600}>
                    {filterType === "home-visitor"
                        ? "Home Team Total Rebounds"
                        : filterType === "winner-loser"
                        ? "Winning Team Total Rebounds"
                        : "Team 1 Total Rebounds"}
                </Text>

                {sliders &&<RangeSlider
                    minRange={0}
                    max={100}
                    color="blue"
                    value={[team1Filter.trb_min!, team1Filter.trb_max!]}
                    onChange={(value) =>
                        setTeam1Filter((prev) => ({
                            ...prev,
                            trb_min: value[0],
                            trb_max: value[1],
                        }))
                    }
                    marks={[
                    { value: 0, label: "0" },
                    { value: 100, label: "100" },
                    ]}
                />}
                <Group grow mt="xs">
                    <NumberInput
                    min={0}
                    max={100}
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
                    max={100}
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
                </Grid.Col>

                <Grid.Col span={{ base: 12, sm: 6 }}>
                <Text fw={600}>
                    {filterType === "home-visitor"
                        ? "Visiting Team Total Rebounds"
                        : filterType === "winner-loser"
                        ? "Losing Team Total Rebounds"
                        : "Team 2 Total Rebounds"}
                </Text>
                {sliders && <RangeSlider
                    minRange={0}
                    max={100}
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
                    ]}
                />}
                <Group grow mt="xs">
                    <NumberInput
                    min={0}
                    max={100}
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
                    max={100}
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
                </Grid.Col>
                {/* <Button onClick={() => setTotReboundsFilter(!totReboundsFilter)} mt="md" variant={!totReboundsFilter ? "filled" : "light"}>
                    {totReboundsFilter ? "Remove Total Rebounds Filter" : "Add Total Rebounds Filter"}
                </Button> */}
            </Grid>}

            {/* Off Rebounds Filters */}
            {activeFilters.includes("off rebounds") && <Grid className="filter-grid" gutter="md">
                <Grid.Col span={{ base: 12, sm: 6 }}>
                <Text fw={600}>
                    {filterType === "home-visitor"
                        ? "Home Team Offensive Rebounds"
                        : filterType === "winner-loser"
                        ? "Winning Team Offensive Rebounds"
                        : "Team 1 Offensive Rebounds"}
                </Text>

                {sliders &&<RangeSlider
                    minRange={0}
                    max={40}
                    color="blue"
                    value={[team1Filter.orb_min!, team1Filter.orb_max!]}
                    onChange={(value) =>
                        setTeam1Filter((prev) => ({
                            ...prev,
                            orb_min: value[0],
                            orb_max: value[1],
                        }))
                    }
                    marks={[
                    { value: 0, label: "0" },
                    { value: 40, label: "40" },
                    ]}
                />}
                <Group grow mt="xs">
                    <NumberInput
                    min={0}
                    max={40}
                    value={team1Filter.orb_min}
                    onChange={(value) =>
                        setTeam1Filter((prev) => ({
                            ...prev,
                            orb_min: Number(value)
                        }))
                    }
                    label="Min"
                    />
                    <NumberInput
                    min={0}
                    max={40}
                    value={team1Filter.orb_max}
                    onChange={(value) =>
                        setTeam1Filter((prev) => ({
                            ...prev,
                            orb_max: Number(value),
                        }))
                    }
                    label="Max"
                    />
                </Group>
                </Grid.Col>

                <Grid.Col span={{ base: 12, sm: 6 }}>
                <Text fw={600}>
                    {filterType === "home-visitor"
                        ? "Visiting Team Offensive Rebounds"
                        : filterType === "winner-loser"
                        ? "Losing Team Offensive Rebounds"
                        : "Team 2 Offensive Rebounds"}
                </Text>
                {sliders && <RangeSlider
                    minRange={0}
                    max={40}
                    color="blue"
                    value={[team2Filter.orb_min!, team2Filter.orb_max!]}
                    onChange={(value) =>
                        setTeam2Filter((prev) => ({
                            ...prev,
                            orb_min: value[0],
                            orb_max: value[1],
                        }))
                    }
                    marks={[
                    { value: 0, label: "0" },
                    { value: 40, label: "40" },
                    ]}
                />}
                <Group grow mt="xs">
                    <NumberInput
                    min={0}
                    max={40}
                    value={team2Filter.orb_min}
                    onChange={(value) =>
                        setTeam2Filter((prev) => ({
                            ...prev,
                            orb_min: Number(value)
                        }))
                    }
                    label="Min"
                    />
                    <NumberInput
                    min={0}
                    max={40}
                    value={team2Filter.orb_max}
                    onChange={(value) =>
                        setTeam2Filter((prev) => ({
                            ...prev,
                            orb_max: Number(value),
                        }))
                    }
                    label="Max"
                    />
                </Group>
                </Grid.Col>
                {/* <Button onClick={() => setTotReboundsFilter(!totReboundsFilter)} mt="md" variant={!totReboundsFilter ? "filled" : "light"}>
                    {totReboundsFilter ? "Remove Total Rebounds Filter" : "Add Total Rebounds Filter"}
                </Button> */}
            </Grid>}

            {/* Def Rebounds Filters */}
            {activeFilters.includes("def rebounds") && <Grid className="filter-grid" gutter="md">
                <Grid.Col span={{ base: 12, sm: 6 }}>
                <Text fw={600}>
                    {filterType === "home-visitor"
                        ? "Home Team Defensive Rebounds"
                        : filterType === "winner-loser"
                        ? "Winning Team Defensive Rebounds"
                        : "Team 1 Defensive Rebounds"}
                </Text>

                {sliders &&<RangeSlider
                    minRange={0}
                    max={60}
                    color="blue"
                    value={[team1Filter.drb_min!, team1Filter.drb_max!]}
                    onChange={(value) =>
                        setTeam1Filter((prev) => ({
                            ...prev,
                            drb_min: value[0],
                            drb_max: value[1],
                        }))
                    }
                    marks={[
                    { value: 0, label: "0" },
                    { value: 60, label: "60" },
                    ]}
                />}
                <Group grow mt="xs">
                    <NumberInput
                    min={0}
                    max={60}
                    value={team1Filter.drb_min}
                    onChange={(value) =>
                        setTeam1Filter((prev) => ({
                            ...prev,
                            drb_min: Number(value)
                        }))
                    }
                    label="Min"
                    />
                    <NumberInput
                    min={0}
                    max={60}
                    value={team1Filter.drb_max}
                    onChange={(value) =>
                        setTeam1Filter((prev) => ({
                            ...prev,
                            drb_max: Number(value),
                        }))
                    }
                    label="Max"
                    />
                </Group>
                </Grid.Col>

                <Grid.Col span={{ base: 12, sm: 6 }}>
                <Text fw={600}>
                    {filterType === "home-visitor"
                        ? "Visiting Team Defensive Rebounds"
                        : filterType === "winner-loser"
                        ? "Losing Team Defensive Rebounds"
                        : "Team 2 Defensive Rebounds"}
                </Text>
                {sliders && <RangeSlider
                    minRange={0}
                    max={60}
                    color="blue"
                    value={[team2Filter.drb_min!, team2Filter.drb_max!]}
                    onChange={(value) =>
                        setTeam2Filter((prev) => ({
                            ...prev,
                            drb_min: value[0],
                            drb_max: value[1],
                        }))
                    }
                    marks={[
                    { value: 0, label: "0" },
                    { value: 60, label: "60" },
                    ]}
                />}
                <Group grow mt="xs">
                    <NumberInput
                    min={0}
                    max={60}
                    value={team2Filter.drb_min}
                    onChange={(value) =>
                        setTeam2Filter((prev) => ({
                            ...prev,
                            drb_min: Number(value)
                        }))
                    }
                    label="Min"
                    />
                    <NumberInput
                    min={0}
                    max={60}
                    value={team2Filter.drb_max}
                    onChange={(value) =>
                        setTeam2Filter((prev) => ({
                            ...prev,
                            drb_max: Number(value),
                        }))
                    }
                    label="Max"
                    />
                </Group>
                </Grid.Col>
                {/* <Button onClick={() => setTotReboundsFilter(!totReboundsFilter)} mt="md" variant={!totReboundsFilter ? "filled" : "light"}>
                    {totReboundsFilter ? "Remove Total Rebounds Filter" : "Add Total Rebounds Filter"}
                </Button> */}
            </Grid>}
                    
            {/* Assists Filters */}
            {activeFilters.includes("assists") && <Grid className="filter-grid" gutter="md">
                <Grid.Col span={{ base: 12, sm: 6 }}>
                <Text fw={600}>
                    {filterType === "home-visitor"
                        ? "Home Team Assists"
                        : filterType === "winner-loser"
                        ? "Winning Team Assists"
                        : "Team 1 Assists"}
                </Text>

                {sliders &&<RangeSlider
                    minRange={0}
                    max={60}
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
                    { value: 60, label: "60" },
                    ]}
                />}
                <Group grow mt="xs">
                    <NumberInput
                    min={0}
                    max={60}
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
                    max={60}
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
                </Grid.Col>

                <Grid.Col span={{ base: 12, sm: 6 }}>
                <Text fw={600}>
                    {filterType === "home-visitor"
                        ? "Visiting Team Assists"
                        : filterType === "winner-loser"
                        ? "Losing Team Assists"
                        : "Team 2 Assists"}
                </Text>
                {sliders && <RangeSlider
                    minRange={0}
                    max={60}
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
                    { value: 60, label: "60" },
                    ]}
                />}
                <Group grow mt="xs">
                    <NumberInput
                    min={0}
                    max={60}
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
                    max={60}
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
                </Grid.Col>
            </Grid>}
            
            {/* Steals Filters */}
            {activeFilters.includes("steals") && <Grid className="filter-grid" gutter="md">
                <Grid.Col span={{ base: 12, sm: 6 }}>
                <Text fw={600}>
                    {filterType === "home-visitor"
                        ? "Home Team Steals"
                        : filterType === "winner-loser"
                        ? "Winning Team Steals"
                        : "Team 1 Steals"}
                </Text>

                {sliders &&<RangeSlider
                    minRange={0}
                    max={30}
                    color="blue"
                    value={[team1Filter.stl_min!, team1Filter.stl_max!]}
                    onChange={(value) =>
                        setTeam1Filter((prev) => ({
                            ...prev,
                            stl_min: value[0],
                            stl_max: value[1],
                        }))
                    }
                    marks={[
                    { value: 0, label: "0" },
                    { value: 30, label: "30" },
                    ]}
                />}
                <Group grow mt="xs">
                    <NumberInput
                    min={0}
                    max={30}
                    value={team1Filter.stl_min}
                    onChange={(value) =>
                        setTeam1Filter((prev) => ({
                            ...prev,
                            stl_min: Number(value)
                        }))
                    }
                    label="Min"
                    />
                    <NumberInput
                    min={0}
                    max={30}
                    value={team1Filter.stl_max}
                    onChange={(value) =>
                        setTeam1Filter((prev) => ({
                            ...prev,
                            stl_max: Number(value),
                        }))
                    }
                    label="Max"
                    />
                </Group>
                </Grid.Col>

                <Grid.Col span={{ base: 12, sm: 6 }}>
                <Text fw={600}>
                    {filterType === "home-visitor"
                        ? "Visiting Team Steals"
                        : filterType === "winner-loser"
                        ? "Losing Team Steals"
                        : "Team 2 Steals"}
                </Text>
                {sliders && <RangeSlider
                    minRange={0}
                    max={30}
                    color="blue"
                    value={[team2Filter.stl_min!, team2Filter.stl_max!]}
                    onChange={(value) =>
                        setTeam2Filter((prev) => ({
                            ...prev,
                            stl_min: value[0],
                            stl_max: value[1],
                        }))
                    }
                    marks={[
                    { value: 0, label: "0" },
                    { value: 30, label: "30" },
                    ]}
                />}
                <Group grow mt="xs">
                    <NumberInput
                    min={0}
                    max={30}
                    value={team2Filter.stl_min}
                    onChange={(value) =>
                        setTeam2Filter((prev) => ({
                            ...prev,
                            stl_min: Number(value)
                        }))
                    }
                    label="Min"
                    />
                    <NumberInput
                    min={0}
                    max={30}
                    value={team2Filter.stl_max}
                    onChange={(value) =>
                        setTeam2Filter((prev) => ({
                            ...prev,
                            stl_max: Number(value),
                        }))
                    }
                    label="Max"
                    />
                </Group>
                </Grid.Col>
            </Grid>}
            
            {/* Blocks Filters */}
            {activeFilters.includes("blocks") && <Grid className="filter-grid" gutter="md">
                <Grid.Col span={{ base: 12, sm: 6 }}>
                <Text fw={600}>
                    {filterType === "home-visitor"
                        ? "Home Team Blocks"
                        : filterType === "winner-loser"
                        ? "Winning Team Blocks"
                        : "Team 1 Blocks"}
                </Text>

                {sliders &&<RangeSlider
                    minRange={0}
                    max={30}
                    color="blue"
                    value={[team1Filter.blk_min!, team1Filter.blk_max!]}
                    onChange={(value) =>
                        setTeam1Filter((prev) => ({
                            ...prev,
                            blk_min: value[0],
                            blk_max: value[1],
                        }))
                    }
                    marks={[
                    { value: 0, label: "0" },
                    { value: 30, label: "30" },
                    ]}
                />}
                <Group grow mt="xs">
                    <NumberInput
                    min={0}
                    max={30}
                    value={team1Filter.blk_min}
                    onChange={(value) =>
                        setTeam1Filter((prev) => ({
                            ...prev,
                            blk_min: Number(value)
                        }))
                    }
                    label="Min"
                    />
                    <NumberInput
                    min={0}
                    max={30}
                    value={team1Filter.blk_max}
                    onChange={(value) =>
                        setTeam1Filter((prev) => ({
                            ...prev,
                            blk_max: Number(value),
                        }))
                    }
                    label="Max"
                    />
                </Group>
                </Grid.Col>

                <Grid.Col span={{ base: 12, sm: 6 }}>
                <Text fw={600}>
                    {filterType === "home-visitor"
                        ? "Visiting Team Blocks"
                        : filterType === "winner-loser"
                        ? "Losing Team Blocks"
                        : "Team 2 Blocks"}
                </Text>
                {sliders && <RangeSlider
                    minRange={0}
                    max={30}
                    color="blue"
                    value={[team2Filter.blk_min!, team2Filter.blk_max!]}
                    onChange={(value) =>
                        setTeam2Filter((prev) => ({
                            ...prev,
                            blk_min: value[0],
                            blk_max: value[1],
                        }))
                    }
                    marks={[
                    { value: 0, label: "0" },
                    { value: 30, label: "30" },
                    ]}
                />}
                <Group grow mt="xs">
                    <NumberInput
                    min={0}
                    max={30}
                    value={team2Filter.blk_min}
                    onChange={(value) =>
                        setTeam2Filter((prev) => ({
                            ...prev,
                            blk_min: Number(value)
                        }))
                    }
                    label="Min"
                    />
                    <NumberInput
                    min={0}
                    max={30}
                    value={team2Filter.blk_max}
                    onChange={(value) =>
                        setTeam2Filter((prev) => ({
                            ...prev,
                            blk_max: Number(value),
                        }))
                    }
                    label="Max"
                    />
                </Group>
                </Grid.Col>
            </Grid>}
            
            {/* Turnovers Filters */}
            {activeFilters.includes("turnovers") && <Grid className="filter-grid" gutter="md">
                <Grid.Col span={{ base: 12, sm: 6 }}>
                <Text fw={600}>
                    {filterType === "home-visitor"
                        ? "Home Team Turnovers"
                        : filterType === "winner-loser"
                        ? "Winning Team Turnovers"
                        : "Team 1 Turnovers"}
                </Text>

                {sliders &&<RangeSlider
                    minRange={0}
                    max={40}
                    color="blue"
                    value={[team1Filter.to_min!, team1Filter.to_max!]}
                    onChange={(value) =>
                        setTeam1Filter((prev) => ({
                            ...prev,
                            to_min: value[0],
                            to_max: value[1],
                        }))
                    }
                    marks={[
                    { value: 0, label: "0" },
                    { value: 40, label: "40" },
                    ]}
                />}
                <Group grow mt="xs">
                    <NumberInput
                    min={0}
                    max={40}
                    value={team1Filter.to_min}
                    onChange={(value) =>
                        setTeam1Filter((prev) => ({
                            ...prev,
                            to_min: Number(value)
                        }))
                    }
                    label="Min"
                    />
                    <NumberInput
                    min={0}
                    max={40}
                    value={team1Filter.to_max}
                    onChange={(value) =>
                        setTeam1Filter((prev) => ({
                            ...prev,
                            to_max: Number(value),
                        }))
                    }
                    label="Max"
                    />
                </Group>
                </Grid.Col>

                <Grid.Col span={{ base: 12, sm: 6 }}>
                <Text fw={600}>
                    {filterType === "home-visitor"
                        ? "Visiting Team Turnovers"
                        : filterType === "winner-loser"
                        ? "Losing Team Turnovers"
                        : "Team 2 Turnovers"}
                </Text>
                {sliders && <RangeSlider
                    minRange={0}
                    max={40}
                    color="blue"
                    value={[team2Filter.to_min!, team2Filter.to_max!]}
                    onChange={(value) =>
                        setTeam2Filter((prev) => ({
                            ...prev,
                            to_min: value[0],
                            to_max: value[1],
                        }))
                    }
                    marks={[
                    { value: 0, label: "0" },
                    { value: 40, label: "40" },
                    ]}
                />}
                <Group grow mt="xs">
                    <NumberInput
                    min={0}
                    max={40}
                    value={team2Filter.to_min}
                    onChange={(value) =>
                        setTeam2Filter((prev) => ({
                            ...prev,
                            to_min: Number(value)
                        }))
                    }
                    label="Min"
                    />
                    <NumberInput
                    min={0}
                    max={40}
                    value={team2Filter.to_max}
                    onChange={(value) =>
                        setTeam2Filter((prev) => ({
                            ...prev,
                            to_max: Number(value),
                        }))
                    }
                    label="Max"
                    />
                </Group>
                </Grid.Col>
            </Grid>}

            {activeFilters.length > 0 && <Button onClick={filter} mt="md">
                Filter
            </Button>}

            {games.length > 0 &&<Text size="lg" fw={700} mt="xl" mb="sm">
                Filtered Games
            </Text>}

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

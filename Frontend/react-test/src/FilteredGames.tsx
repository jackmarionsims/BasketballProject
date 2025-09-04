
import React, { useState } from "react";
import {Table, Loader, Alert, NumberInput, RangeSlider, Button, Group, Container, Grid, Text, Card, Checkbox, Stack} from "@mantine/core";
import StatFilter from "./StatFilter";
import { getFilteredGames, type FilterParams } from "./api";
import { Link } from "react-router-dom";
import './App.css';

export function formatDate(dateString: string): string {
    const date = new Date(dateString);

    // Use Intl API for proper formatting
    return date.toLocaleDateString("en-US", {
        year: "numeric",
        month: "long",
        day: "numeric",
    });
}

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
        tov_min: 0,
        tov_max: 40
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
        tov_min: 0,
        tov_max: 40
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
            {activeFilters.includes("points") && StatFilter(
                { statKey: "pts",
                    label: "Points",
                    team1Filter,
                    setTeam1Filter,
                    team2Filter,
                    setTeam2Filter,
                    filterType,
                    sliders,
                    max: 200
                }
            )}

            {/* Tot Rebounds Filters */}
            {activeFilters.includes("tot rebounds") && StatFilter({
                statKey: "trb",
                label: "Total Rebounds",
                team1Filter,
                setTeam1Filter,
                team2Filter,
                setTeam2Filter,
                filterType,
                sliders,
                max: 100
            })}

            {/* Off Rebounds Filters */}
            {activeFilters.includes("off rebounds") && StatFilter({
                statKey: "orb",
                label: "Offensive Rebounds",
                team1Filter,
                setTeam1Filter,
                team2Filter,
                setTeam2Filter,
                filterType,
                sliders,
                max: 40
            })}

            {/* Def Rebounds Filters */}
            {activeFilters.includes("off rebounds") && StatFilter({
                statKey: "drb",
                label: "Defensive Rebounds",
                team1Filter,
                setTeam1Filter,
                team2Filter,
                setTeam2Filter,
                filterType,
                sliders,
                max: 60
            })}
                    
            {/* Assists Filters */}
            {activeFilters.includes("assists") && StatFilter({
                statKey: "ast",
                label: "Assists",
                team1Filter,
                setTeam1Filter,
                team2Filter,
                setTeam2Filter,
                filterType,
                sliders,
                max: 60
            })}
            
            {/* Steals Filters */}
            {activeFilters.includes("steals") && StatFilter({
                statKey: "stl",
                label: "Steals",
                team1Filter,
                setTeam1Filter,
                team2Filter,
                setTeam2Filter,
                filterType,
                sliders,
                max: 30
            })}
            
            {/* Blocks Filters */}
            {activeFilters.includes("blocks") && StatFilter({
                statKey: "blk",
                label: "Blocks",
                team1Filter,
                setTeam1Filter,
                team2Filter,
                setTeam2Filter,
                filterType,
                sliders,
                max: 30
            })}
            
            {/* Turnovers Filters */}
            {activeFilters.includes("turnovers") && StatFilter({
                statKey: "tov",
                label: "Turnovers",
                team1Filter,
                setTeam1Filter,
                team2Filter,
                setTeam2Filter,
                filterType,
                sliders,
                max: 40
            })}

            {/* Blocks Filters */}
            {activeFilters.includes("blocks") && StatFilter({
                statKey: "blk",
                label: "Blocks",
                team1Filter,
                setTeam1Filter,
                team2Filter,
                setTeam2Filter,
                filterType,
                sliders,
                max: 30
            })}

            {/* FGA Filters */}
            {activeFilters.includes("fga") && StatFilter({
                statKey: "fga",
                label: "Field Goal Attempts",
                team1Filter,
                setTeam1Filter,
                team2Filter,
                setTeam2Filter,
                filterType,
                sliders,
                max: 150
            })}

            {/* FGM Filters */}
            {activeFilters.includes("fgm") && StatFilter({
                statKey: "fgm",
                label: "Field Goals Made",
                team1Filter,
                setTeam1Filter,
                team2Filter,
                setTeam2Filter,
                filterType,
                sliders,
                max: 80
            })}

            {/* FG% Filters */}
            {activeFilters.includes("fg%") && StatFilter({
                statKey: "fg_pct",
                label: "Field Goal %",
                team1Filter,
                setTeam1Filter,
                team2Filter,
                setTeam2Filter,
                filterType,
                sliders,
                max: 100
            })}

            {/* Fouls Filters */}
            {activeFilters.includes("fouls") && StatFilter({    
                statKey: "fouls",
                label: "Fouls",
                team1Filter,
                setTeam1Filter,
                team2Filter,
                setTeam2Filter,
                filterType,
                sliders,
                max: 60
            })}

            {/* FTA Filters */}
            {activeFilters.includes("fta") && StatFilter({
                statKey: "fta",
                label: "Free Throw Attempts",
                team1Filter,
                setTeam1Filter,
                team2Filter,
                setTeam2Filter,
                filterType,
                sliders,
                max: 80
            })}

            {/* FTM Filters */}
            {activeFilters.includes("ftm") && StatFilter({
                statKey: "ftm",
                label: "Free Throws Made",
                team1Filter,
                setTeam1Filter,
                team2Filter,
                setTeam2Filter,
                filterType,
                sliders,
                max: 80
            })}

            {/* FT% Filters */}
            {activeFilters.includes("ft%") && StatFilter({
                statKey: "ft_pct",
                label: "Free Throw %",
                team1Filter,
                setTeam1Filter,
                team2Filter,
                setTeam2Filter,
                filterType,
                sliders,
                max: 100
            })}

            {/* 3PA Filters */}
            {activeFilters.includes("3pa") && StatFilter({
                statKey: "tpa",
                label: "3 Point Attempts",
                team1Filter,
                setTeam1Filter,
                team2Filter,
                setTeam2Filter,
                filterType,
                sliders,
                max: 80
            })}

            {/* 3PM Filters */}
            {activeFilters.includes("3pm") && StatFilter({
                statKey: "tpm",
                label: "3 Pointers Made",
                team1Filter,
                setTeam1Filter,
                team2Filter,
                setTeam2Filter,
                filterType,
                sliders,
                max: 40
            })}

            {/* 3P% Filters */}
            {activeFilters.includes("3p%") && StatFilter({
                statKey: "tp_pct",
                label: "3 Point %",
                team1Filter,
                setTeam1Filter,
                team2Filter,
                setTeam2Filter,
                filterType,
                sliders,
                max: 100
            })}


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
                    <td>{formatDate(game["Date"])}</td>
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

import { useParams, useSearchParams } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { Table, Text, Title, Loader, Center, Paper, Container, Button } from "@mantine/core";
import { getGame, getPrediction } from './api'
import { formatDate } from './FilteredGames';

interface GameData {
    "Game ID": string;
    "Date Number": number;
    "Date": string;
    "Game Type": string;
    "Home Team": string;
    "Visitor Team": string;
    "Winner": string;
    "Loser": string;
    "Home Win": number;
    "Home Team PTS": number;
    "Home Team AST": number;
    "Home Team TRB": number;
    "Home Team ORB": number;
    "Home Team DRB": number;
    "Home Team BLK": number;
    "Home Team STL": number;
    "Home Team FGA": number;
    "Home Team FG": number;
    "Home Team FG%": number;
    "Home Team 3PA": number;
    "Home Team 3P": number;
    "Home Team 3P%": number;
    "Home Team FTA": number;
    "Home Team FT": number;
    "Home Team FT%": number;
    "Home Team PF": number;
    "Home Team TOV": number;
    "Visitor Team PTS": number;
    "Visitor Team AST": number;
    "Visitor Team TRB": number;
    "Visitor Team ORB": number;
    "Visitor Team DRB": number;
    "Visitor Team BLK": number;
    "Visitor Team STL": number;
    "Visitor Team FGA": number;
    "Visitor Team FG": number;
    "Visitor Team FG%": number;
    "Visitor Team 3PA": number;
    "Visitor Team 3P": number;
    "Visitor Team 3P%": number;
    "Visitor Team FTA": number;
    "Visitor Team FT": number;
    "Visitor Team FT%": number;
    "Visitor Team PF": number;
    "Visitor Team TOV": number;
    "Playoff Game": number;
    "Season": number;
    [key: string]: number | string;
}


export default function GameDetails() {
    const { gameId } = useParams();
    const [searchParams] = useSearchParams();
    const boxScoreOnly = searchParams.get("box_score_only") === "true";
    const [gameData, setGameData] = useState<GameData | null>(null);
    const [homeWinProb, setHomeWinProb] = useState<number | null>(null);
    const [homeScore, setHomeScore] = useState<number | null>(null);
    const [visitorScore, setVisitorScore] = useState<number | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        getGame(String(gameId), boxScoreOnly).then((result) => {
            setGameData(result);
        }).catch((err) => {
            console.error(err);
        }).finally(() => {
            setLoading(false);
        });
    }, [gameId]);

    if (loading) {
        return (
        <Center style={{ height: "100%" }}>
            <Loader />
        </Center>
        );
    }

    if (!gameData) {
        return <Text c="red">Failed to load game data.</Text>;
    }

    // const boxScore = gameData.box_score.box_score;
    // const pregame = gameData.pregame_stats.pgs;

    const groupedStats: Record<string, { Visitor: number | string; Home: number | string }> = {};

    Object.entries(gameData).forEach(([key, value]) => {
        if (key.includes("Visitor Team ")) {
            const statName = key.replace("Visitor Team ", "");
            if (!groupedStats[statName]) groupedStats[statName] = { Visitor: "", Home: "" };
            console.log(value, typeof(value))
            groupedStats[statName].Visitor = value;
        } else if (key.includes("Home Team ")) {
            const statName = key.replace("Home Team ", "");
            if (!groupedStats[statName]) groupedStats[statName] = { Visitor: "", Home: "" };
            groupedStats[statName].Home = value;
        }
        console.log(groupedStats)
    });
    for (const key of ["3P%", "FG%", "FT%"]){ // "ORB%", "TO%", "FTM/FGA", "TS%"
        
        if (groupedStats[key]) {
            const home = groupedStats[key].Home;
            const visitor = groupedStats[key].Visitor;
            groupedStats[key].Home = typeof home === "number" ? home.toFixed(3) : home;
            groupedStats[key].Visitor = typeof visitor === "number" ? visitor.toFixed(3) : visitor;
        }
    }

    return (
        <Container size="lg" mt="xl">
            <Paper shadow="md" p="md" radius="md" style={{ margin: "0 auto" }}>
                <Title order={1}>
                    {gameData["Visitor Team"]} @ {gameData["Home Team"]}
                </Title>
                <Title order={3}>
                    {gameData.Season - 1}-{gameData.Season} : {formatDate(gameData.Date)}
                </Title>

                {/* Box Score Table */}
                <Table striped highlightOnHover mt="md">
                    <thead>
                    <tr>
                        <th></th>
                        <th>{gameData["Visitor Team"]}</th>
                        <th>{gameData["Home Team"]}</th>
                    </tr>
                    </thead>
                    <tbody>
                    {Object.entries(groupedStats).map(([stat, values]) => (
                        <tr key={stat}>
                        <td>
                            <Text fw={500}>{stat}</Text>
                        </td>
                        <td>{values.Visitor}</td>
                        <td>{values.Home}</td>
                        </tr>
                    ))}
                    </tbody>
                </Table>
            </Paper>
            {/* <Button onClick={() => getPrediction(Number(gameId)).then((result) => {
                    setHomeWinProb(Number(result.home_win_probability))
                    setHomeScore(Number(result.predicted_home_score))
                    setVisitorScore(Number(result.predicted_visitor_score))
                })} mt="md">
                    Predict Winner
            </Button>
            {homeWinProb !== null && (
                <Text mt="md" size="lg">
                    Predicted Winner: {homeWinProb > 0.5 ? gameData.pregame_stats.pgs["Home Team"] : gameData.pregame_stats.pgs["Visitor Team"]} with probability {(homeWinProb > 0.5 ? homeWinProb : 1 - homeWinProb).toFixed(2)}
                </Text>
            )}
            {homeScore !== null && visitorScore !== null && (
                <Text mt="md" size="lg">
                    Predicted Score: {gameData.pregame_stats.pgs["Home Team"]} {homeScore} - {gameData.pregame_stats.pgs["Visitor Team"]} {visitorScore}
                </Text>
            )} */}
        </Container>
        );

}

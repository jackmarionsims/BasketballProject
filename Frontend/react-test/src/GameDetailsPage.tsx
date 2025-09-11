import { useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { Table, Text, Title, Loader, Center, Paper, Container, Button } from "@mantine/core";
import { getGame, getPrediction } from './api'
import { formatDate } from './FilteredGames';

export default function GameDetails() {
    const { gameId } = useParams();
    const [gameData, setGameData] = useState<any>(null);
    const [homeWinProb, setHomeWinProb] = useState<number | null>(null);
    const [homeScore, setHomeScore] = useState<number | null>(null);
    const [visitorScore, setVisitorScore] = useState<number | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        getGame(Number(gameId)).then((result) => {
            setGameData(result);
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

    const boxScore = gameData.box_score.box_score;
    const pregame = gameData.pregame_stats.pgs;

    const groupedStats: Record<string, { Visitor: number | string; Home: number | string }> = {};

    Object.entries(boxScore).forEach(([key, value]) => {
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
        
        groupedStats[key].Home = groupedStats[key].Home.toFixed(2)
        groupedStats[key].Visitor = groupedStats[key].Visitor.toFixed(2)
    }

    return (
        <Container size="lg" mt="xl">
            <Paper shadow="md" p="md" radius="md" style={{ margin: "0 auto" }}>
                <Title order={1}>
                    {pregame["Visitor Team"]} @ {pregame["Home Team"]}
                </Title>
                <Title order={3}>
                    {pregame.Season - 1}-{pregame.Season} : {formatDate(pregame.Date)}
                </Title>

                {/* Box Score Table */}
                <Table striped highlightOnHover mt="md">
                    <thead>
                    <tr>
                        <th></th>
                        <th>{boxScore["Visitor Team"]}</th>
                        <th>{boxScore["Home Team"]}</th>
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
            <Button onClick={() => getPrediction(Number(gameId)).then((result) => {
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
            )}
        </Container>
        );

}

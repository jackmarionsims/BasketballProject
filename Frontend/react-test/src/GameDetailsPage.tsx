import { useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { Table, Text, Title, Loader, Center, Paper, Container } from "@mantine/core";
import { getGame } from './api'

export default function GameDetails() {
    const { gameId } = useParams();
    const [gameData, setGameData] = useState<any>(null);
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
    for (const key of ["3P%", "FG%", "FT%", "ORB%", "TO%", "FTM/FGA", "TS%"]){
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
                {pregame.Year - 1}-{pregame.Year} : {pregame.Date}
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
        </Container>
        );

}

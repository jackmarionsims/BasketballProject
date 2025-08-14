const BASE_URL = "http://localhost:8000"; // your FastAPI URL

export type FilterParams = {
    // Points
    pts_min?: number;
    pts_max?: number;

    // Assists
    ast_min?: number;
    ast_max?: number;

    // Total rebounds
    trb_min?: number;
    trb_max?: number;

    // Offensive rebounds
    orb_min?: number;
    orb_max?: number;

    // Defensive rebounds
    drb_min?: number;
    drb_max?: number;

    // Blocks
    blk_min?: number;
    blk_max?: number;

    // Steals
    stl_min?: number;
    stl_max?: number;

    // Field goals attempted
    fga_min?: number;
    fga_max?: number;

    // Field goals made
    fgm_min?: number;
    fgm_max?: number;

    // Field goal %
    fg_pct_min?: number;
    fg_pct_max?: number;

    // Three-point attempts
    tpa_min?: number;
    tpa_max?: number;

    // Three-point makes
    tpm_min?: number;
    tpm_max?: number;

    // Three-point %
    tp_pct_min?: number;
    tp_pct_max?: number;

    // Free throw attempts
    fta_min?: number;
    fta_max?: number;

    // Free throw makes
    ftm_min?: number;
    ftm_max?: number;

    // Free throw %
    ft_pct_min?: number;
    ft_pct_max?: number;

    // Fouls
    fouls_min?: number;
    fouls_max?: number;

    // Turnovers
    to_min?: number;
    to_max?: number;
};
export async function getTeam(teamName: string, season: number) {
    const res = await fetch(`${BASE_URL}/${teamName}?season=${season}`);
    if (!res.ok) {
        throw new Error(`Error fetching data: ${res.statusText}`);
    }
    return res.json();
}

export async function getGame(gameId: number) {
    const res = await fetch(`${BASE_URL}/game/${gameId}`);
    if (!res.ok) {
        throw new Error(`Error fetching data: ${res.statusText}`);
    }
    return res.json();
}

export async function getFilteredGames(
    filter1: FilterParams,
    filter2: FilterParams,
    filterType: string,
    marginFilter?: FilterParams,
) {
    const params = new URLSearchParams();
    // Append home_filter fields
    for (const [key, value] of Object.entries(filter1)) {
        if (value !== undefined) {
            params.append(`team1_${key}`, String(value));
        }
    }

    // Append visitor_filter fields
    for (const [key, value] of Object.entries(filter2)) {
        if (value !== undefined) {
            params.append(`team2_${key}`, String(value));
        }
    }
    console.log(params.toString())
    if (filterType === "home-visitor" || filterType === "winner-loser") {
        const res = await fetch(`${BASE_URL}/filter-${filterType}?${params.toString()}`); 
        if (!res.ok) throw new Error(`Error ${res.status}`);
        // console.log(res.json())
        return res.json();
    }
    else {
        const res = await fetch(`${BASE_URL}/filter?${params.toString()}`);
        if (!res.ok) throw new Error(`Error ${res.status}`);
        // console.log(res.json())
        return res.json();
    }
}
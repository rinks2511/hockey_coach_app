/**
 * Application State Store Module
 * Manages active team context, rosters, and tactical board configuration.
 */

const state = {
    currentTeam: localStorage.getItem('hv_myra_active_team') || 'MO10',
    currentUserRole: 'parent',
    coachEmails: JSON.parse(localStorage.getItem('hv_myra_coaches')) || ["singhalrajeev89@gmail.com"],
    squadPlayers: [],
    customPositionNames: {},
    activeFormation: '1-2-3-2',
    currentAssignments: {},
    drawnTactics: [],
    subMatrixState: {}
};

export function getState() {
    return state;
}

export function setActiveTeam(teamId) {
    state.currentTeam = teamId;
    localStorage.setItem('hv_myra_active_team', teamId);
}

export function setSquadPlayers(players) {
    state.squadPlayers = players;
}

export function setCoachEmails(emails) {
    state.coachEmails = emails;
    localStorage.setItem('hv_myra_coaches', JSON.stringify(emails));
}

export function setCustomPositionNames(positions) {
    state.customPositionNames = positions;
}

export function setActiveFormation(formation) {
    state.activeFormation = formation;
}

export function setAssignments(assignments) {
    state.currentAssignments = assignments;
}

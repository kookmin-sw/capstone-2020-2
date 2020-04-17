import axios from "axios";

export const getLogin = () => async dispatch => {
	const res = await axios.get("/api/v1/login");
	dispatch({
		type: "GET_LOGIN",
		payload: res.data
	});
};

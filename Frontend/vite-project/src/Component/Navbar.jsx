import { Link } from "react-router-dom";
import { Comment_Text } from "./Comment_Text";

export function Navbar({accesstoken}) {


    const clearAccess = () => {
        window.localStorage.setItem("accesstoken", '')
    }


    return (
        <>
            <Link to='/'>
                <button className="btn btn-dark" onClick={clearAccess}>登出</button>
            </Link>
            <Comment_Text accesstoken={accesstoken}/>
        </>
    )
}
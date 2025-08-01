import { Link } from "react-router-dom";

export function Navbar() {


    const clearAccess = () => {
        window.localStorage.setItem("accesstoken", '')
    }


    return (
        <>
            <Link to='/'>
                <button className="btn btn-dark" onClick={clearAccess}>登出</button>
            </Link>
        </>
    )
}
import { useState} from "react";
import Data_Format from '../Config'

export function User() {
    const url_default = Data_Format["url_default"]
    const [username, setUserame] = useState("");
    const [password, setPassword] = useState("");
    const [key, setKey] = useState("");

    const [isRegister, setIsRegister] = useState(false)
    const [isSuccess, setIsSuccess] = useState(false)
    const [resultText, setresultText] = useState('')
    const [isOpenAlert, setIsOpenAlert] = useState(false)

    const [isLogin, setIsLogin] = useState(false)


    
    const [Accesstoken, setAccessToken] = useState('')
    window.localStorage.setItem("accesstoken", Accesstoken)




    const onLogin = async () => {
        const data = isRegister ? {
            "username":username,
            "password":password,
            "key":key
        } : 
        {
            "username":username,
            "password":password,
        }
        const options = {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        }
        const url = isRegister ? `${url_default}/register` : `${url_default}/login`
        const response = await fetch(url, options)
        const msg = await response.json()
        setresultText(msg.message)
        if (response.status === 201) {
            setIsSuccess(true)
            if (!isRegister) {
                setAccessToken(msg.access_token)
                setIsLogin(true)
            } else {
                alert("註冊成功，請重新登入")
                window.location.reload()
            }
        } else {
            setIsSuccess(false)
        }
        setIsOpenAlert(true)
    }
    
    const onLogout = async () => {
        const options = {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${Accesstoken}`
            },
        }
        const url = `${url_default}/logout`
        const response = await fetch(url, options)
        const msg = await response.json()
        setresultText(msg.message)
        if (response.status === 200) {
            window.location.reload() //這是登出
        } else {
            setIsSuccess(false)
        }
        setIsOpenAlert(true)
    }

    return (
        <>
            <div className="container">
                <div className="row row-cols-1 gy-5">
                    <div className='col'>
                        {isOpenAlert && 
                            <div className={isSuccess ? "alert alert-success alert-dismissible":"alert alert-danger alert-dismissible"} role="alert">
                                <h1>{isSuccess? '操作成功':'操作失敗'}</h1>
                                {isSuccess ? 
                                <a href={isLogin && "#/LearnList"} className="alert-link">{isLogin && "點我進入列表"}</a>
                                :
                                `錯誤訊息:${resultText}`
                                }
                                <button className="btn-close" data-bs-dismiss="alert"></button>
                            </div>  
                        }
                    </div>
                    <div className='col'>
                        <div className="card">
                            <div className="btn-group">
                                <button onClick={() => setIsRegister(false)} className={isRegister? "btn btn-secondary":"btn btn-info"} type="submit" disabled={isLogin}>登入</button>
                                <button onClick={() => setIsRegister(true)} className={isRegister? "btn btn-info":"btn btn-secondary"} type="submit" disabled={isLogin}>註冊</button>
                            </div>
                            <div className="card-body">
                                <form onSubmit={!isLogin? onLogin : onLogout}>
                                        <div className="input-group">
                                            <input  onChange={(e) => setUserame(e.target.value)}  type={isSuccess ? "hidden":"text"} required className="form-control learn" placeholder="name:使用者名稱 (訪客帳號=XXX)" />
                                            <input  onChange={(e) => setPassword(e.target.value)}  type={isSuccess ? "hidden":"text"} required className="form-control learn" placeholder="password:密碼 (訪客密碼=XXXXX)"/>
                                            {
                                                isRegister && <input onChange={(e) => setKey(e.target.value)}  type={isSuccess ? "hidden":"text"} required className="form-control learn" placeholder="key:授權碼"/>
                                            }
                                        </div>
                                    {isLogin ? 
                                    <button className="btn btn-warning" type="submit">登出</button>
                                    :
                                    <button className="btn btn-info" type="submit">{isRegister ? '註冊':'登入'}</button>
                                    }
                                    
                                </form> 
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </>
    )
}

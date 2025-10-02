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




    const onLogin = async (e) => {
        e.preventDefault()
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
    
    const onLogout = async (e) => {
        e.preventDefault()
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
                    <div class="card text-bg-success bg-opacity-25">
                        <div class="card-body">
                            <div className='col'><h2>網頁操作步驟</h2></div>
                            <div className='col'>Step1: 註冊帳號(授權碼需詢問)</div>
                            <div className='col'>Step2: 登入</div>
                            <div className='col'>Step3: 於上方表格新增項目</div>
                            <div className='col'>Step4: 點選'編輯'按鈕可分別更改項目參數</div>
                            <div className='col'>Step5: 點選'標籤'按鈕能讓項目增添數個標籤，並可編輯標籤</div>
                            <div className='col'>Step6: 按下'顯示標籤'可篩選下方列表顯示</div>
                        </div>
                        <div class="card-body">
                            <div className='col'><h2>使用範例與資源:透過登入訪客帳號查閱(密碼皆輸入test即可)</h2></div>
                            <div className='col'><h2>以下訪客帳號擇一登入</h2></div>
                            <div className='col'>說明_參考資源</div>
                            <div className='col'>說明_標籤系統</div>
                            <div className='col'>說明_路由</div>
                            <div className='col'>範例_日本旅遊</div>
                            <div className='col'>範例_日語學習</div>
                            <div className='col'>範例_程式架構_pytest</div>
                        </div>
                    </div>
                </div>
            </div>
        </>
    )
}

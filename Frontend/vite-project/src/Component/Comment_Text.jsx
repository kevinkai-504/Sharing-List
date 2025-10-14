import { useState, useEffect } from "react";
import Data_Format from '../Config'
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';

export function Comment_Text({accesstoken}) {
    const [comment, setComment] = useState("說明欄待補充")
    const [iscommentchange, setIscommentchange] = useState(false)
    // Modal
    const [show, setShow] = useState(false);
    const handleClose = () => {
        setShow(false);
        setIscommentchange(false)
    }
    const handleShow = () => setShow(true);

    useEffect(() => {
    fetchcomment();
    }, []);



    const url_defalut = Data_Format["url_default"]
    const fetchcomment = async () => {
        const url = `${url_defalut}/usercomment`
        const options = {
            method: "GET",
            headers: {
                'Authorization': `Bearer ${accesstoken}`
            }
        }

        const response = await fetch(url, options)
        const data = await response.json()
        setComment(data['comment'])
    }

    const changecomment = async (e) => {
        e.preventDefault()
        const url = `${url_defalut}/usercomment`
        const options = {
            method: "PUT",
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accesstoken}`
            },
            body: JSON.stringify({ comment: comment })
        }

        const response = await fetch(url, options)
        const data = await response.json()
        if (response.status !== 200) {
            alert(data.message)
            setIscommentchange(false)
        } else {
            setComment(data['comment'])
            setIscommentchange(true)
        }
    }

    return (
        <>

            <Button variant="primary" onClick={handleShow}>
                說明
            </Button>

            <Modal show={show} onHide={handleClose}>
                <Modal.Header closeButton>
                <Modal.Title>列表說明與編輯</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <div className="container">
                        <div className="row row-cols-1 gy-5">
                            <form onSubmit={changecomment}>
                                {iscommentchange && 
                                    <label className="form-label text-danger">已變更為{comment}!!</label>
                                }
                                <div className="input-group">
                                    <input onChange={(e) => setComment(e.target.value)} value={comment}  type="text"  className="form-control"/>
                                </div>
                                <button className="btn btn-info" type="submit">變更</button>
                            </form>
                            <div className="card-body">
                                <div className='col'><h2>網頁操作<span className="text-success fw-bold">步驟</span></h2></div>
                                <div className='col'><span className="text-success fw-bold">Step1: 註冊帳號(授權碼需詢問)</span></div>
                                <div className='col'><span className="text-success fw-bold">Step2: 登入</span></div>
                                <div className='col'><span className="text-success fw-bold">Step3: 於上方表格新增項目</span></div>
                                <div className='col'><span className="text-success fw-bold">Step4: 點選'編輯'按鈕可分別更改項目參數、'刪除'按鈕進行項目刪除</span></div>
                                <div className='col'><span className="text-success fw-bold">Step5: 點選'標籤'按鈕能讓項目增添數個標籤，並可編輯標籤</span></div>
                                <div className='col'><span className="text-success fw-bold">Step6: 按下'顯示標籤'可篩選下方列表顯示</span></div>
                                <div className='col'><span className="text-success fw-bold">Step7: 按下'說明'可觀看該列表的說明與進行編輯</span></div>
                                <div className='col'><span className="text-success fw-bold">Step8: 按下'登出'可順利登出</span></div>
                            </div>
                        </div>
                    </div>
                </Modal.Body>
            </Modal>
        </>
    )
}




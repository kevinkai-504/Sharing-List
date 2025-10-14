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
                        <form onSubmit={changecomment}>
                            {iscommentchange && 
                                <label className="form-label text-danger">已變更為{comment}!!</label>
                            }
                            <div className="input-group">
                                <input onChange={(e) => setComment(e.target.value)} value={comment}  type="text"  className="form-control"/>
                            </div>
                            <button className="btn btn-success" type="submit">變更</button>
                        </form>
                    </div>
                </Modal.Body>
            </Modal>
        </>
    )
}




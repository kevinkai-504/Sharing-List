
// Modal外觀直接取自document: https://react-bootstrap.netlify.app/docs/components/modal/
import { useState, useEffect} from 'react';
import Data_Format from '../Config'
import Modal from 'react-bootstrap/Modal';
import { TagList_Input } from './TagList_Input';
import { Item_List } from './Item_List';




export function Modal_view({type, type2='', link_id='', link_type='', name, recover, accesstoken}) {


  useEffect(() => {
    fetchItems(type);
  }, [])

  const url_defalut = Data_Format["url_default"]
  const [items, setItems] = useState({
    data: [],
    attributes: [],
  });
  const fetchItems = async (target) => {
    const url = `${url_defalut}/${target}`
    const options = {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${accesstoken}`
            },
    }
    const response = await fetch(url, options);
    const datas = await response.json();
    setItems({
      ...items,
      data: datas,
      attributes: Data_Format[target],
      type:target
    });
  };
  const onUpdate = (target) => {
    fetchItems(target);
  }

  const handleClose = () => {
    setShow(false)
    recover(false)
  }

  const [show, setShow] = useState(true);
  return (
  <>
      <Modal show={show} fullscreen={true} onHide={() => handleClose()}>
      <Modal.Header closeButton>
          <Modal.Title>{name}(標籤編輯)</Modal.Title>
      </Modal.Header>
      <Modal.Body>
          <div className='container'>
              <div className="row row-cols-1 gy-5">
                  <div className='col'>
                      <TagList_Input updateCall={() => onUpdate(type)} type={items.type} accesstoken={accesstoken}/> 
                  </div>
                  <div className="col">
                      <Item_List datas={items.data} attributes={items.attributes} updateCall={() => onUpdate(type)} type={items.type} type2={type2} link_id={link_id} link_type={link_type} accesstoken={accesstoken}/>
                  </div>
              </div>
          </div>
      </Modal.Body>
      </Modal>
  </>
  );
}

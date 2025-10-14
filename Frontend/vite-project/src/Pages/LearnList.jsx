import { useState, useEffect} from 'react'
import { LearnList_Input } from '../Component/LearnList_Input'
import Data_Format from '../Config'
import { Item_List } from '../Component/Item_List'

import { Navbar } from '../Component/Navbar'


export function LearnList({}) {
  const [tag_list, setTag_list] = useState([])
  const accesstoken = window.localStorage.getItem("accesstoken")

  useEffect(() => {
    fetchItems("learnFtag", tag_list);
  }, [tag_list])


  
  const url_defalut = Data_Format["url_default"]
  const [items, setItems] = useState({
    data: [],
    attributes: [],
  });
  const fetchItems = async (target, tag_list=[]) => {
    const url = `${url_defalut}/${target}`
    const options = {     //為了有篩選標籤的效果所以才出現post，不然其實都是get來得到數據就好
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            'Authorization': `Bearer ${accesstoken}`
        },
        body: JSON.stringify({"tag_list":tag_list})
    }
    const response = (target != 'learnFtag') ? await fetch(url) : await fetch(url, options)  //這是特例，現在沒有在使用後端learn路由來進行get method(1)
    const datas = await response.json();
    setItems({
      ...items,
      data: datas,
      attributes: Data_Format[target],
      type:(target === 'learnFtag') ? 'learn':target    //這是特例，現在沒有在使用後端learn路由來進行get method(2)
    });
  };
  const onUpdate = (target, tag_list) => {
    fetchItems(target, tag_list);
  }



// 以下為額外的篩選功能
  const [tag_list_set, setTag_list_set] = useState(new Set()) //為了得到標籤篩選(與Button_list配合)
  const [openList, setOpenList] = useState(false)
  const [buttons, setButtons] = useState([])

  const fetchButtons = async (target) => {
    const url = `${url_defalut}/${target}`
    const options = {
      method: 'GET',
      headers: {
          'Authorization': `Bearer ${accesstoken}`
      },
    }
    const response = await fetch(url, options)
    const datas = await response.json()
    setButtons(datas)
  }
  const ButtonArray = (target) => {
      if (!openList) {
        fetchButtons(target);
        setOpenList(!openList);
      } else {
        setTag_list([])
        setTag_list_set(new Set())
        setOpenList(!openList)
        onUpdate('learnFtag', tag_list)
      }
  }
  const onFilter = (id) => {
    !tag_list_set.has(id) ? tag_list_set.add(id) : tag_list_set.delete(id)
    setTag_list_set(tag_list_set)
    setTag_list(Array.from(tag_list_set))
  }



  return (
    <>
      <Navbar accesstoken={accesstoken}/>
      {/* {accesstoken} */}
      <div className='container'>
        <div className="row row-cols-1 gy-5">
          <div className='col'>
            <LearnList_Input updateCall={() => onUpdate('learnFtag')} type={items.type} accesstoken={accesstoken}/>
          </div>

          <div className="col">
            <button className={openList? "btn btn-warning":"btn btn-success"} onClick={() => ButtonArray('tag')}>{openList? "取消顯示":"顯示標籤"}</button>
            {openList && buttons.map((button) => (
                <button className={tag_list_set.has(button.id) ? "btn btn-success":"btn btn-secondary"} onClick={() => onFilter(button.id)}>
                  {button.name}
                </button>
            ))}
          </div>

          <div className="col">
            <Item_List datas={items.data} attributes={items.attributes} updateCall={() => onUpdate('learnFtag', tag_list)} type={items.type} type2={"tag"} accesstoken={accesstoken}/>
          </div>
        </div>
      </div>
    </>
  )
}


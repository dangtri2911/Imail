import React, {useState} from 'react';

export default class ListMailServices {
    
    static getListMail = async(api__) => {
        return await fetch(api__)
    }
}

# FitnessWS
Web Service for the project FitnessApp

This web service is available here : http://psotty.pythonanywhere.com

<ol>
  <li>
  <b>It allows to get data in json format for the FitnessApp project:</b>
    <ul>
      <li>List of sports (methods=['GET']): http://psotty.pythonanywhere.com/sports<br/>
      Result : {"sports": [{"id": 12, "name": "bike", "units": [4,5,3]}, ...]}
      </li>
      <li>List of units (methods=['GET']): http://psotty.pythonanywhere.com/units<br/>
      Result : {"units": [{"code": "h", "id": 4, "name": "hour"}, ...]}
      </li>
      <li>List of sessions of a specific user : [incoming]</li>
    </ul>
  </li>
  <li>
  <b>It allows to add data in json format to the MySQL DataBase :</b>
    <ul>
      <li>
      Add a sport (methods=['POST']): http://psotty.pythonanywhere.com/sports<br/>
        Body : {"name": "bike", "units": [{"unit_id": 4},{"unit_id": 5},{"unit_id": 3}]}
      </li>
      <li>
      Add a unit (methods=['POST']): http://psotty.pythonanywhere.com/units<br/>
        Body : {"code": "h", "name": "hour"}
      </li>
      <li>
      Add a user (methods=['POST']): [incoming]
      </li>
      <li>
      Add a session (methods=['POST']): [incoming]
      </li>
    </ul>
  </li>
</ol>

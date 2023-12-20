function getClasses() {
  username = localStorage.getItem('username')
  var params = {"userName": username};

  const classes = sdk.userNameGet(params, {}, {})
    .then((res) => {
      if (res.status == 200) {
        return res.data;
      }
    }).catch( () => {
    console.log("failed");
    }
  )

  return classes;
}

function uploadFileToS3() {
  var file = document.getElementById('userFile').files[0];
  
  if (file) {
    // Read the file content as a binary data
    var reader = new FileReader();
    reader.onload = function (event) {
      // Convert the binary data to ArrayBuffer
      var fileData = event.target.result;
      var params = {
        "userName": 'ap2963',
        "courseName": 'csgy9223',
        "fileName": file.name
      };
      var additionalParams = {};

      var fileSizeInBytes = file.size;
      var fileSizeInMB = fileSizeInBytes / (1024 * 1024);
      console.log(fileSizeInMB);

      if (fileSizeInMB < 10) {
        sdk.userNameCourseNameFileNamePut(params, fileData, additionalParams)
          .then(function (res) {
            if (res.status == 200) {
              console.log(res.status);
            }
          }).catch(() => {
            console.log("upload failed");
          }
        );
      } else {
        // sdk GET bigfile
        sdk.userNameCourseNameBigFileFileNameGet(params, fileData, additionalParams)
          .then(function (res) {
            if (res.status == 200) {
              console.log(res.status);
              presignedURL = res.body;

              const uploadFile = async (presignedURL, fileData) => {
                const result = await Axios.put(presignedURL, fileData, {
                  headers: {
                    "x-api-key": 'wbv9kvsPu16Z7axKFfi7phdarNFuAGZ71y62Ilv1',
                    "Content-Type": "application/octet-stream"
                  }
                }).catch(error => console.error(error.response.data, {request: error.request}));
            
                console.info(result.data);
                return result.data;
              };
            }
          }).catch(() => {
            console.log("big file upload failed");
          }
        );
      }}
    reader.readAsArrayBuffer(file);
  } else {
    console.error('No file selected.');
  }
}

function createNewClass() {
  var classLabel1Value = document.getElementById('classLabel1').value.trim();
  var classLabel2Value = document.getElementById('classLabel2').value.trim();

  if (!classLabel1Value || classLabel1Value.length === 0) {
    alert("You must provide a class title");
    return false;
  }

  if (divElement.textContent.trim().length > 0) 

  var params = {
    "userName": 'ap2963', 
    "className": classLabel1Value
  };

  sdk.userNameCreateCoursePost(params, {}, {})
    .then(function (result) {
      console.log('Folder created successfully:', result);
      alert("Success!");
    })
    .catch(function (error) {
      console.error('Error:', error);
      alert("Error");
    });
}

function displaySummary(text) {
  for (var i=0; i < text.length; i++) {
    if (text[i].length > 0) {
      var newSection = document.createElement('div');
      newSection.className = 'text-section';
      newSection.innerHTML = "<p>" + text[i] + "<p>"
      document.getElementById('summaryContainer').appendChild(newSection);
    }
  }
}

function getTextFile(path) {
  var request = new XMLHttpRequest();
  request.open('GET', path, true);
  request.send(null);
  request.onreadystatechange = function () {
    if (request.readyState === 4 && request.status === 200) {
      var type = request.getResponseHeader('Content-Type');
      if (type.indexOf("text") !== 1) {
        var outer_text = request.responseText;
        console.log(typeof(outer_text));
        outer_text = outer_text.split('\n'); 
        console.log(outer_text.length);
        console.log(outer_text[0]);
        displaySummary(outer_text);
      }
    }
  }
}

function getSummary(courseName, fileName) {
  const uName = localStorage.getItem('username');
  const cName = courseName;
  const fName = fileName;

  console.log(courseName)

  var params = {
    'userName': uName,
    'courseName': cName,
    'fileName': fName
  }

  sdk.userNameCourseNameFileNameGet(params, {}, {})
    .then((res) => {
      if (res.status == 200) {
        url = res.data['summary_url'];
        getTextFile(url);
      }
    }).catch( () => {
      console.log("failed");
    }
  );
}

function populateFileTable(arr) {
  const tableBody = document.getElementById('fileTableBody');

  // Clear existing rows
  tableBody.innerHTML = '';

  // Iterate through the array and create table rows
  arr.forEach(fileInfo => {
    const row = document.createElement('tr');
    const titleCell = document.createElement('td');
    const uploadDateCell = document.createElement('td');
    const summaryCell = document.createElement('td');

    // Fill in cell content
    titleCell.textContent = arr['File Name & Type'];
    uploadDateCell.textContent = arr['Date Uploaded'];
    summaryCell.textContent = arr['Summary Available'];

    // Append cells to the row
    row.appendChild(titleCell);
    row.appendChild(uploadDateCell);
    row.appendChild(summaryCell);

    // Append the row to the table body
    tableBody.appendChild(row);
    });
}


function getCourseContent() {
  const uName = 'jr6594',
  cName = 'csgy9223';
  var content = [];

  var params = {
    'userName': uName,
    'courseName': cName
  }

  sdk.userNameCourseNameGet(params, {}, {})
    .then((res) => {
      if (res.status == 200) {
        console.log(res.data);
        for (var i=0; i < res.data.length; i++) {
          const seed = new Date().getTime();
          Math.seedrandom(seed);
          const randomNumber = Math.random();
          const today = new Date();
          const formattedDate = `${today.getMonth() + 1}-${last14Days.getDate()}-${last14Days.getFullYear()}`;

          content[i] = {'File Name & Type': res.data[i], 'Date Uploaded': formattedDate, 'Summary Available': Boolean(randomNumber >= 0.5)};
        }
        populateFileTable(content)
      }
    }).catch( () => {
      console.log("failed");
    }
    
  );
  
}

async function authenticateUser(params) {
  let data = new FormData()
  data.append("email", params['email'])
  data.append("password", params['password'])

  let fetchFormEncodedRequest = {
    method: "POST",
    body: data
  }

  fetch('http://127.0.0.1:5000/login', fetchFormEncodedRequest).then(function(res) {
    if (res.status === 200) {
      res.json().then(function(data)
      {
        console.log(data);
        localStorage.setItem('email', params['email'])
        window.location.replace('./home.html')
      })
    }
  })
}

function registerUser(params) {
  let data = new FormData()
  data.append("fname", params['fname'])
  data.append("lname", params['lname'])
  data.append("email", params['email'])
  data.append("password", params['password'])
  data.append("street", params['street'])
  data.append("city", params['city'])
  data.append("state", params['state'])
  data.append("zipcode", params['zipcode'])

  let fetchFormEncodedRequest = {
    method: "POST",
    body: data
  }

  fetch('http://127.0.0.1:5000/registerUser', fetchFormEncodedRequest).then(function(res) {
    if (res.status === 200) {
      res.json().then(function(data)
      {
        console.log(data);
        localStorage.setItem('email', params['email']);
        window.location.replace('./home.html');
      })
    }
  })
}

function getFileList(params) {
  const fileList = sdk.userNameCourseNameGet(params, {}, {}).then((res => {
    if (res.status === 200) {
      return res['data'];
    }
  })).catch( () => {
    console.log("failed");
    });

    return fileList;
}



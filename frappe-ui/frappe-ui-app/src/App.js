import logo from './logo.svg';
import './App.css';
import React, { useState, useEffect } from 'react';

function App() {
  const [bookData, setBookData] = useState({
    title: '',
    author: '',
    publisher: '',
    requirement: 0
  });

  const [showSearchResults, setShowSearchResults] = useState(false);

  const handleInputChange = (e) => {
    setBookData({ ...bookData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:8000/storeBooks', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(bookData)
      });
      const data = await response.json();
      console.log(data); // Optionally, do something with the response data
      alert(data.message)
    } catch (error) {
      console.error(error);
    }
  };

  const [books, setBooks] = useState([]);
  const [searchCriteria, setSearchCriteria] = useState({
    title: '',
    author: ''
  });

  useEffect(() => {
    if (showSearchResults) {
      fetchBooks();
    }
  }, [showSearchResults]);

  const fetchBooks = async () => {
    try {
      let url = 'http://localhost:8000/getBooks';
      if (searchCriteria.title || searchCriteria.author) {
        url += `?title=${searchCriteria.title}&author=${searchCriteria.author}`;
      }
      const response = await fetch(url);
      const data = await response.json();
      setBooks(data.res);
      console.log(books);
      alert(data.res)
    } catch (error) {
      console.error(error);
    }
  };

  const handleInputChangeSearch = (e) => {
    setSearchCriteria({ ...searchCriteria, [e.target.name]: e.target.value });
  };

  const handleSubmitSearch = (e) => {
    e.preventDefault();
    // fetchBooks();
    setShowSearchResults(true);
  };


  const [email, setEmail] = useState('');
  const [registrationStatus, setRegistrationStatus] = useState('');

  const handleInputChangeOnRegistration = (e) => {
    setEmail(e.target.value);
  };

  const handleRegistration = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch('http://localhost:8000/registerMembers', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email })
      });

      const data = await response.json();
      setRegistrationStatus(data.res);
      alert(data.res)
    } catch (error) {
      console.error(error);
    }
  };


  const [issue_email, setIssueEmail] = useState('');
  const [title, setTitle] = useState('');
  const [issueStatus, setIssueStatus] = useState('');

  const handleEmailChange = (e) => {
    setIssueEmail(e.target.value);
  };

  const handleTitleChange = (e) => {
    setTitle(e.target.value);
  };

  const handleSubmitIssueBook = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch('http://localhost:8000/issueBooks', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ issue_email, title })
      });

      const data = await response.json();
      setIssueStatus(data.res);
      alert(data.res)
    } catch (error) {
      console.error(error);
    }
  };

  const [return_member_email, setReturnMemberEmail] = useState('');
  const [return_book_title, setReturnBookTitle] = useState('');
  const [returnStatus, setReturnStatus] = useState('');

  const handleReturnEmailChange = (e) => {
    setReturnMemberEmail(e.target.value);
  };

  const handleReturnTitleChange = (e) => {
    setReturnBookTitle(e.target.value);
  };

  const handleReturnSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch('http://localhost:8000/returnBook', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ return_member_email, return_book_title })
      });

      const data = await response.json();
      setReturnStatus(data.res);
      alert(data.res)
    } catch (error) {
      console.error(error);
    }
  };

  const [delete_member_email, setDeleteMemberEmail] = useState('');
  const [deleteStatus, setDeleteStatus] = useState('');

  const handleDeleteMemberEmailChange = (e) => {
    setDeleteMemberEmail(e.target.value);
  };

  const handleDeleteMemberSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch('http://localhost:8000/deleteMember', {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ delete_member_email })
      });

      const data = await response.json();
      setDeleteStatus(data.res);
      alert(data.res)
    } catch (error) {
      console.error(error);
    }
  };

  const [delete_book_title, setDeleteBookTitle] = useState('');
  const [deleteBookStatus, setDeleteBookStatus] = useState('');

  const handleDeletBookTitleChange = (e) => {
    setDeleteBookTitle(e.target.value);
  };

  const handleDeleteBookSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch('http://localhost:8000/deleteBook', {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ delete_book_title })
      });

      const data = await response.json();
      setDeleteBookStatus(data.res);
      alert(data.res)
    } catch (error) {
      console.error(error);
    }
  };


  return (
    <div>
      <div>
        <h2>Add Book to Store</h2>
        <form onSubmit={handleSubmit}>
          <div>
            <label>Title:</label>
            <input type="text" name="title" value={bookData.title} onChange={handleInputChange} />
          </div>
          <div>
            <label>Author:</label>
            <input type="text" name="author" value={bookData.author} onChange={handleInputChange} />
          </div>
          <div>
            <label>Publisher:</label>
            <input type="text" name="publisher" value={bookData.publisher} onChange={handleInputChange} />
          </div>
          <div>
            <label>Requirement:</label>
            <input
              type="number"
              name="requirement"
              value={bookData.requirement}
              onChange={handleInputChange}
            />
          </div>
          <button type="submit">Add Book</button>
        </form>
      </div>

      <div>
      <h2>Search Books</h2>
      <form onSubmit={handleSubmitSearch}>
        <div>
          <label>Title:</label>
          <input
            type="text"
            name="title"
            value={searchCriteria.title}
            onChange={handleSubmitSearch}
          />
        </div>
        <div>
          <label>Author:</label>
          <input
            type="text"
            name="author"
            value={searchCriteria.author}
            onChange={handleInputChangeSearch}
          />
        </div>
        <button type="submit">Search</button>
      </form>

      {showSearchResults && (
        <div>
          <h2>Search Results</h2>
          {books.map((book) => (
            <div key={book.id}>
              <p>Title: {book.title}</p>
              <p>Author: {book.author}</p>
            </div>
          ))}
        </div>
      )}
    </div>

    <div>
      <h2>Member Registration</h2>
      <form onSubmit={handleRegistration}>
        <div>
          <label>Email:</label>
          <input
            type="email"
            name="email"
            value={email}
            onChange={handleInputChangeOnRegistration}
          />
        </div>
        <button type="submit">Register</button>
      </form>

      {registrationStatus && <p>{registrationStatus}</p>}
    </div>


    <div>
      <h2>Book Issuance</h2>
      <form onSubmit={handleSubmitIssueBook}>
        <div>
          <label>Email:</label>
          <input
            type="email"
            name="email"
            value={issue_email}
            onChange={handleEmailChange}
          />
        </div>
        <div>
          <label>Title:</label>
          <input
            type="text"
            name="title"
            value={title}
            onChange={handleTitleChange}
          />
        </div>
        <button type="submit">Issue Book</button>
      </form>

      {issueStatus && <p>{issueStatus}</p>}
    </div>

    <div>
      <h2>Book Return</h2>
      <form onSubmit={handleReturnSubmit}>
        <div>
          <label>Email:</label>
          <input
            type="email"
            name="email"
            value={return_member_email}
            onChange={handleReturnEmailChange}
          />
        </div>
        <div>
          <label>Title:</label>
          <input
            type="text"
            name="title"
            value={return_book_title}
            onChange={handleReturnTitleChange}
          />
        </div>
        <button type="submit">Return Book</button>
      </form>

      {returnStatus && <p>{returnStatus}</p>}
    </div>

    <div>
      <h2>Delete Member</h2>
      <form onSubmit={handleDeleteMemberSubmit}>
        <div>
          <label>Email:</label>
          <input
            type="email"
            name="email"
            value={delete_member_email}
            onChange={handleDeleteMemberEmailChange}
          />
        </div>
        <button type="submit">Delete Member</button>
      </form>

      {deleteStatus && <p>{deleteStatus}</p>}
    </div>

    <div>
      <h2>Delete Book</h2>
      <form onSubmit={handleDeleteBookSubmit}>
        <div>
          <label>Title:</label>
          <input
            type="text"
            name="title"
            value={delete_book_title}
            onChange={handleDeletBookTitleChange}
          />
        </div>
        <button type="submit">Delete Book</button>
      </form>

      {deleteBookStatus && <p>{deleteBookStatus}</p>}
    </div>

    </div>
  );
}

export default App;

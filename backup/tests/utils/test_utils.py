import pytest
from backup.github_utils import (
    validate_github_user,
    validate_github_repo,
    validate_username_and_repo_url,
    GITHUB_API_URL,
    GITHUB_BASE_URL
)


@pytest.mark.parametrize("username, expected_url", [
    ("testuser", f"{GITHUB_API_URL}/users/testuser"),
    ("anotheruser", f"{GITHUB_API_URL}/users/anotheruser"),
])
def test_validate_github_user(mocker, username, expected_url):
    mock_get = mocker.patch("backup.github_utils.requests.get")
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"html_url": f"{GITHUB_BASE_URL}/{username}"}  
    response = validate_github_user(username)  
    mock_get.assert_called_once_with(expected_url) 
    assert response.status_code == 200
    

@pytest.mark.parametrize("username, repo_name, expected_url", [
    ("testuser", "testrepo", f"{GITHUB_API_URL}/repos/testuser/testrepo"),
    ("anotheruser",  "anotherrepo", f"{GITHUB_API_URL}/repos/anotheruser/anotherrepo" )
    ])
def test_validate_github_repo(mocker, username, repo_name, expected_url):
    mock_get = mocker.patch("backup.github_utils.requests.get")
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"name":repo_name }
    response = validate_github_repo(username, repo_name)
    mock_get .assert_called_once_with(expected_url)
    assert response.status_code == 200 
 
     
@pytest.mark.parametrize("username, repo_url, expected_valid, expected_message", [
    ("testuser", "https://github.com/testuser/testrepo", True, "testrepo"),
    ("testuser", "https://invalid.com/testuser/testrepo", False, "Invalid GitHub URL base."),
    ("testuser", "https://github.com/otheruser/testrepo", False, "Username in repository URL does not match the provided username."),
    ("testuser", "", False, "Both 'username' and 'github_url' are required."),
    ("", "https://github.com/testuser/testrepo", False, "Both 'username' and 'github_url' are required."),
    ("testuser", "invalid-url", False, "Invalid GitHub repository URL structure."),
])
def test_validate_username_and_repo_url(username, repo_url, expected_valid, expected_message):
    is_valid, message = validate_username_and_repo_url(username, repo_url)
    assert is_valid == expected_valid
    assert message == expected_message
// Функция для открытия модального окна редактирования пользователя
function openEditUserModal(user) {
    const modal = document.getElementById('editUserModal');
    if (user.id) {
      // Заполняем форму данными пользователя
      document.getElementById('editUserId').value = user.id;
      document.getElementById('editUserName').value = user.full_name;
      document.getElementById('editUserType').value = user.type;
      document.getElementById('editUserEmail').value = user.email;
      document.getElementById('editUserPhone').value = user.phone;
    } else {
      // Очищаем форму для добавления нового пользователя
      document.getElementById('editUserId').value = '';
      document.getElementById('editUserName').value = '';
      document.getElementById('editUserType').value = '';
      document.getElementById('editUserEmail').value = '';
      document.getElementById('editUserPhone').value = '';
    }
    modal.classList.remove('hidden');
  }
  
  // Функция для сохранения пользователя
  async function saveUser(event) {
    event.preventDefault();
  
    const userId = document.getElementById('editUserId').value;
    const fullName = document.getElementById('editUserName').value;
    const type = document.getElementById('editUserType').value;
    const email = document.getElementById('editUserEmail').value;
    const phone = document.getElementById('editUserPhone').value;
  
    const userData = {
      id: userId,
      full_name: fullName,
      type: type,
      email: email,
      phone: phone,
    };
  
    try {
      const response = await fetch('/save_user', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
      });
  
      if (response.ok) {
        // Закрываем модальное окно и обновляем таблицу
        closeModal('editUserModal');
        window.location.reload(); // Перезагружаем страницу для обновления данных
      } else {
        alert('Ошибка при сохранении пользователя');
      }
    } catch (error) {
      console.error('Ошибка:', error);
    }
  }
  
  // Функция для удаления пользователя
  async function deleteUser(userId) {
    if (confirm('Вы уверены, что хотите удалить этого пользователя?')) {
      try {
        const response = await fetch(`/delete_user/${userId}`, {
          method: 'DELETE',
        });
  
        if (response.ok) {
          // Обновляем таблицу
          window.location.reload(); // Перезагружаем страницу для обновления данных
        } else {
          alert('Ошибка при удалении пользователя');
        }
      } catch (error) {
        console.error('Ошибка:', error);
      }
    }
  }
  
  // Функция для закрытия модального окна
  function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    modal.classList.add('hidden');
  }
  
  // Назначаем обработчики событий
  document.addEventListener('DOMContentLoaded', () => {
    // Обработчик для формы сохранения пользователя
    document.getElementById('editUserForm').addEventListener('submit', saveUser);
  
    // Обработчик для кнопки закрытия модального окна
    document.getElementById('closeEditUserModal').addEventListener('click', () => closeModal('editUserModal'));
  });
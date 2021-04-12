/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: evirgili <evirgili@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2020/11/26 19:13:30 by evirgili          #+#    #+#             */
/*   Updated: 2020/12/03 15:52:05 by evirgili         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "get_next_line.h"

static int		ft_gnlwhile(int fd, char **line, char **str, char **rest)
{
	int			ret;
	char		buf[BUFFER_SIZE + 1];
	char		*free_str;

	while ((ret = read(fd, buf, BUFFER_SIZE)))
	{
		if (ret == -1)
			return (-1);
		buf[ret] = '\0';
		free_str = *str;
		*str = ft_strjoin(*str, buf);
		free(free_str);
		if (ft_strchr(buf, '\n'))
		{
			*rest = ft_strdup(ft_strchr(buf, '\n') + 1);
			*ft_strchr(*str, '\n') = '\0';
			*line = *str;
			return (1);
		}
	}
	*line = *str;
	return (0);
}

int				get_next_line(int fd, char **line)
{
	int			ret;
	static char	*rest[1024] = {0};
	char		*str;

	if (fd < 0 || line == NULL || BUFFER_SIZE < 1)
		return (-1);
	if (rest[fd])
	{
		str = rest[fd];
		rest[fd] = 0;
	}
	else
		str = ft_strdup("");
	if (ft_strchr(str, '\n'))
	{
		rest[fd] = ft_strdup(ft_strchr(str, '\n') + 1);
		*ft_strchr(str, '\n') = '\0';
		*line = ft_strdup(str);
		free(str);
		return (1);
	}
	ret = ft_gnlwhile(fd, line, &str, &(rest[fd]));
	return (ret);
}
